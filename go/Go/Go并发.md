# Go并发 

Go语言区别于其他语言的一大特点就是出色的并发性能，最重要的一个特性那就是`go`关键字。

并发场景：

- UI小姐姐一边开着PS软件，一边微信疯狂的和产品经理打字交流，后台还听着网易云音乐。。
- 双11当天。。大伙疯狂的访问淘宝网站
- CPU从单核向多核发展，计算机程序不该是串行的，浪费资源
- 串行程序由于IO操作被阻塞，整个程序处于停滞状态，其他IO无关的任务无法执行

并发必要性：

- 充分利用CPU核心的优势，提高程序执行效率

实现并发的模型：

- 多进程，多进程是在操作系统层面并发的基本模式，进程间互不影响，但是开销最大，进程由内核管理。
- 多线程，属于系统层面的并发模式，也是用的最多的有效模式，大多数软件使用多线程，开销小于多进程。
- 基于回调的非阻塞/异步IO。此架构处于多线程模式的危机，高并发服务器下，多线程会消耗殆尽服务器的内存和CPU资源。而通过事件驱动的方式使用异步IO，尽可能少用线程，降低开销，Node.js就是如此实践，但是此模式编程复杂度较高。
- **协程**，Coroutine是一种用户态线程，寄存于线程中，系统开销极小，可以有效提高线程任务并发性，使用方式简单，结构清晰，避免多线程的缺点。需要编程语言的支持，如不支持，需要用户自行实现调度器。

`共享内存系统`是比较常用的并发模式，线程之间通信采用共享内存的方式，程序员需要加锁等操作避免死锁、资源竞争等问题。

计算机科学家又研制出了`消息传递系统`，`对线程间共享状态的各种操作被封装在线程之间传递的消息中`。

Communicating Sequential Processes（**顺序通信进程**），在CSP系统中，所有的并发操作都是通过独立线程以异步的方式运行，这些线程必须通过再彼此之间发送消息，从而向另一个线程请求信息。

## 进程和线程

`进程`是程序在操作系统中的一次执行过程，是系统进行资源分配和调度的基本单位。

`线程`是进程的一个执行实例，是比进程更小的独立运行的基本单位。

进程可以创建或销毁多个线程，同一个进程中的多个线程可以并发执行（如百度云盘进程中的，多个下载任务）。

一个程序至少一个进程，一个进程至少一个线程。

![](/media/uploads/2019/03/_book/Chapter8/pic/1.png)

------

## 并发和并行

1）多线程程序在单核CPU上运行，就是`并发`

2）多线程程序在多核CPU上运行，就是`并行`

![](/media/uploads/2019/03/_book/Chapter8/pic/5.png)

------

![](/media/uploads/2019/03/_book/Chapter8/pic/2.png)

为何人们常说提升`并发`，而不是提升`并行`？

因为`并发`是通过`时间片轮转`进行进程调度，是通过技术手段提升并发。

而`并行`是通过硬件提升效率，有钱人可以买一个128核的服务器。

------

## 协程是什么

执行单位是个抽象的概念，操作系统层面有多个概念与之对应，比如操作系统掌管的进程（process）、进程内的线程（thread）以及`进程内的协程（coroutine）`。

协程在于`轻量级`，轻松创建`百万个`而不会导致系统资源衰竭。

多数语言语法层面不直接支持协程，而是通过库的方式支持，然而库的功能也仅仅是线程的创建、销毁与切换，而无法达到协程调用同一个IO操作，如网络通信，文件读写等。

## goroutine

Golang在语言层面支持协程，名为`goroutine`，Go语言标准库提供所有系统调用操作，都会让出CPU给其他goroutine，使得协程切换管理不依赖于系统的线程和进程，也不依赖于CPU核数。

一个Go进程，可以启动多个goroutine协程。

一个普通的机器运行几十个线程负载已经很高了，然而可以轻松创建`百万个`goroutine。

go标准库的net包，写出的go web server性能直接媲美Nginx。

------

![](/media/uploads/2019/03/_book/Chapter8/pic/3.png)

------

## goroutine入门

第一个goroutine，开启协程，执行函数hello()

```
package main

import (
	"fmt"
	"time"
)

func hello() {
	fmt.Println("hello goroutine")
}

func main() {
	go hello()
	fmt.Println("main thread terminate")
	time.Sleep(time.Second)
}
```

批量开启协程

```
package main

import (
	"fmt"
	"time"
)

func hello(i int) {
	fmt.Println("hello goroutine", i)
}

func main() {
	//循环开启10个协程，分别执行hello()函数
	for i := 0; i < 10; i++ {
		go hello(i)
	}
	time.Sleep(time.Second)
}
```



编写代码，完成功能

1.在go主进程中，开启goroutine，该协程`每秒`输出一个`你好，我是goroutine`

2.在主进程中也`每秒`输出一个`我很好，我是主进程`，输出10次后退出程序

3.要求主进程和goroutine同时执行

```
package main

import (
	"fmt"
	"strconv"
	"time"
)

//定义一个协程任务函数
func test() {
	for i := 0; i <= 10; i++ {
		fmt.Println("你好，我是goroutine" + strconv.Itoa(i))
		time.Sleep(time.Second) //睡眠1秒
	}
}

func main() {
	go test()
	for i := 0; i <= 10; i++ {
		fmt.Println("我很好，我是主进程" + strconv.Itoa(i))
		time.Sleep(time.Second) //睡眠1秒
	}
}
```

------

![](/media/uploads/2019/03/_book/Chapter8/pic/4.png)

------

```
提示：检测主进程结束，协程也立即结束，或是检测主进程未结束，协程提前退出，可以修改for循环的次数！
```

## runtime包控制goroutine

runtime.Gosched()让出时间片，如同接力赛跑，让出了接力棒。

gosched如同yield作用，暂停当前的goroutine，放回队列等待下次执行。

```
package main

import (
	"fmt"
	"runtime"
)

func main() {
	go func() {
		for i := 0; i < 5; i++ {
			fmt.Println("你愁啥")
		}
	}()

	for i := 0; i < 2; i++ {
		//让出时间片，让其他协程执行
		runtime.Gosched()
		fmt.Println("尼古拉斯赵四")
	}
}
```

runtime.Goexit()终止当前协程

```
package main

import (
	"fmt"
	"runtime"
	"time"
)

func test() {
	defer fmt.Println("ccc")
	//return  //函数终止，打印a  c  b  结束
	runtime.Goexit() //退出所在协程，  打印 a c  退出主进程
	fmt.Println("ddd")
}

func main() {
	go func() {
		fmt.Println("aaa")
		test()
		fmt.Println("bbb")
	}()
	//
	time.Sleep(time.Second * 3)
}
```

Go与多核的优势，设置cpu运行数目

go version < 1.8 需要手动设置多核

go version > 1.8 默认用多核，无须设置

```
package main

import (
	"fmt"
	"runtime"
)

func main() {
	cpuNum := runtime.NumCPU()
	//可以在这演示下单核时，时间片无切换，仅仅打印数字0的实验 runtime.GOMAXPROCS(1)
	runtime.GOMAXPROCS(cpuNum)
	for i := 0; i < 500; i++ {
		go fmt.Print(1)
		fmt.Print(0)
	}
}
```

## goroutine使用recover

```
package main

import (
	"fmt"
	"time"
)

func test() {
	defer func() {
		if err := recover(); err != nil {
			fmt.Println("出错了：", err)
		}
	}()

	var m map[string]int
	//map必须初始化才能使用
	//m=make(map[string]int,10)
	m["stu"] = 111

}

func calc() {
	for {
		fmt.Println("我是calc函数")
		time.Sleep(time.Second)
	}
}

func main() {
	go test() //协程执行函数，这个函数有错的话,程序会panic退出，做好异常捕捉
	for i := 0; i < 2; i++ {
		go calc()
	}
	time.Sleep(time.Second * 10)
}
```

# 8.2 Go 锁

案例（坑）：多个goroutine操作同一个map。

go提供了一种叫map的数据结构，可以翻译成映射，对应于其他语言的字典、哈希表。借助map，可以定义一个键和值，然后可以从map中获取、设置和删除这个值，尤其适合数据查找的场景。

但是map的使用有一定的限制，如果是在单个协程中读写map，那么不会存在什么问题，`如果是多个协程并发访问一个map`，有可能会导致程序退出，并打印下面错误信息。

```
fatal error: concurrent map writes
```

**错误案例代码**

```
package main

var myMap = make(map[int]int, 10)

//要求计算50的阶乘结果
//阶乘就是1*2*3*4...50 =?

func test(n int) {
	//定义初始值1
	res := 1
	//每次循环进行阶乘
	for i := 0; i <= n; i++ {
		res *= i
	}
	//最终计算结果，写入map
	//由于多个协程同时操作map，引发资源竞争报错
	myMap[n] = res

}
func main() {
	//开启50个协程
	for i := 0; i < 10; i++ {
		go test(10)
	}
}
```

并发访问map是不安全的操作，在`协程`中访问map，必须提供某种`同步资源`机制，使用`sync.Mutex`互斥锁同步解决协程的竞争问题。

```
package main

import (
	"fmt"
	"sync"
	"time"
)

var lock sync.Mutex

func Printer(str string) {
	//我现在开始使用打印机了，其他人都等我完事了再来
	lock.Lock()
	for _, data := range str {
		fmt.Printf("%c", data)
		time.Sleep(time.Second)
	}
	//我完事了，你们上吧
	lock.Unlock()
	fmt.Printf("\n")
}

func Alex() {
	Printer("hello")
}
func Wupeiqi() {
	Printer("oldboy")
}

func main() {
	//coffe(10)//单线程执行函数
	go Alex()
	go Wupeiqi()
	//主线程等待协程结束后 再退出
	time.Sleep(time.Second * 10)
}
```

结论：

```
1.可以使用加锁的方式解决goroutine的通讯。
2.主线程等待所有goroutine的时间难以确定，设置固定的等待时间肯定不合理。
3.对全局变量加锁同步来通讯，也不利于多个协程对变量的读写。
4.要让主线程等待所有goroutine退出后在退出，如何知道所有goroutine都退出了呢？
5.因此，channel应运而生！！
```