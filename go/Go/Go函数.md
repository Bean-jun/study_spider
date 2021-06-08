# Go函数定义

Go函数是指：将一个语句序列打包成一个单元，然后可以在程序中其他地方多次调用。

Go分为自定义函数，系统函数。

函数可以将一个大的工作拆解成小的任务。

函数对用户隐藏了细节。

Golang函数特点：

```
支持不定长参数
支持多返回值
支持命名返回参数
支持匿名函数、闭包
函数也是类型，可以赋值给变量

一个package下不得有两个同名函数，不支持函数重载

函数参数可以没有，或者多个参数
注意类型在变量名后面
多个连续的函数命名参数是同一类型，除了最后一个类型，其余可以省略
函数可以返回任意数量的返回值
函数体中，形参作为局部变量
函数返回值可以用 _标识符进行忽略
```

Go函数基本语法：

1）形参：函数的输入参数

2）执行代码：实现函数功能的代码块

3）函数的返回值可有可无

```
func 函数名(形参列表)(返回值列表){
    执行代码
    return 返回值列表
}

func test(x, y int, z string) (int, string) {
	//类型相同的相邻参数x，y参数类型可以合并
	//多返回值得用括号括起来
	n := x + y
	return n, z
}
```

## 函数实战

```
package main

import "fmt"

//最普通的函数,无参数，无返回值
func sayHello() {
	fmt.Printf("hello world\n")
}

//求和函数add
func add(a, b, c int) int {
	//sum := a + b + c
	//return sum
	return a + b
}

//接收2个参数a 和b都是int类型
//返回2个参数，sum和sub作为返回值，也叫做对返回值命名
func calc(a, b int) (sum int, sub int) {
	sum = a + b
	sub = a - b
	return
}

//接收不定长参数个数，
//参数名是b，类型是不固定个数的int类型
//变量b此时是一个slice切片,数据类型：[]int，可以通过索引取值
func calc_v1(b ...int) int {
	sum := 0
	for i := 0; i < len(b); i++ {
		sum = sum + b[i]
	}
	return sum
}

func main() {
	//调用函数
	sayHello()
	//打印返回值求和结果
	fmt.Println(add(5, 5, 5))

	//多个返回值
	sum1, sub1 := calc(5, 10)
	fmt.Printf("calc计算和是%d\n", sum1)
	fmt.Printf("calc计算差是%d\n", sub1)

	//传入不固定长度的参数个数
	sum := calc_v1(10, 20, 30, 40)
	fmt.Println(sum)

}
```

## Go函数注意事项

1）基本数据类型和数组默认`值传递`，有一个值拷贝过程，不会修改原本变量的值

```
package main

import "fmt"

func modify(n int) {
	n = n + 100
	fmt.Println("modify函数修改后n=", n)
}

func main() {
	num := 10
	modify(num)
	fmt.Println("此时main主程中的nun值=", num)
}
```

2）如果希望函数可以修改函数外的变量，需要以`指针传递`，传入变量的`地址`，函数内以`指针`方式操作变量。

```
package main

import "fmt"

//指针变量，接收一个地址
func modify2(n *int) {
	*n = *n + 100
	fmt.Println("modify2修改后n的值=", *n)
}

func main() {
	num2 := 10
	modify2(&num2)
	fmt.Println("此时main主程中的num2值=", num2)
}
```

## init函数

每个源文件都会包含一个inti函数，该函数在main函数之前被执行。

```
package main

import "fmt"

func init() {
	fmt.Println("init函数一般完成初始化工作，如数据库驱动连接等")
}

func main() {
	fmt.Println("我是主程序")
}
```

## init函数细节

go程序加载流程：

```
全局变量
↓
init函数
↓
main函数
```

```
package main

import "fmt"

//全局变量
var num = test()

func test() int {
	fmt.Println("执行了test()函数")
	return 999
}

func init() {
	fmt.Println("执行了init函数")
}

func main() {
	fmt.Println("我是主程序")
	fmt.Println(num)
}
```

**面试题**：

如果再包导入中，main.go和utils.go都有变量加载，init函数，执行流程是？

```
main.go是程序入口
↓
自上而下，进入import导入
↓
优先进入utils.go 加载全局变量  这是第一步
↓
执行utils.go的init函数		第二步
↓
完毕后，回到main.go的全局变量	第三步
↓
执行main.go的init函数		第四步
↓
执行main.go的主程main()函数	第五步
```

# 5.2 Go 包与函数

在多个包中相互调用函数，需要用到Go包的知识。

代码组织如下：

![](/media/uploads/2019/03/_book/Chapter5/3.png)

思路：

```
1.定义功能函数calc放入到utils.go，将utils.go放在utils文件夹/包中，当其他文件需要引入utils.go时，只需要导入该utils包，即可使用(包名.函数名)
```

代码

main.go

```
package main

import (
	"fmt"
	"gostudy/gobook/funcDemo/utils"
)

//两种方式二选一
//相对路径导入
//import "../utils"

//绝对路径导入，从src目录下开始

func main() {
	//通过utils包访问公开函数Calc
	res := utils.Calc(10, 20)
	fmt.Println(res)
}

```

utils.go

```
package utils

//写一个可导出的函数，需要首字母大写
//给返回值命名n3
func Calc(n1, n2 int) (n3 int) {
	res := n1 + n2
	return res
}

```

包的import方式，详见[章节2.4](../Chapter2/4.md)

## 编译可执行程序

对上述代码编译，需要包声明为main，也就是package main，这是语法规范。

```
go build main.go
```

# 5.3 Go 匿名函数

Go支持匿名函数，顾名思义就是没名字的函数。

匿名函数一般用在，函数只运行一次，也可以多次调用。

匿名函数可以像普通变量一样被调用。

匿名函数由不带函数名字的`函数声明`与`函数体`组成。

```
package main

import "fmt"

func main() {
	//定义匿名函数，接收2个参数n1,n2，返回值int
	res := func(n1, n2 int) int {
		return n1 * n2
	}(10, 20) //匿名函数在此处调用，传参
	fmt.Println("res=", res)
}

```

匿名函数赋值给变量

``局部变量``

```
package main

import "fmt"

func main() {
//局部变量n1
	n1 := func(a, b int) int {
		return a * b
	}
	fmt.Printf("n1的类型:%T\n", n1)
	res := n1(10, 10)
	fmt.Println("res调用结果：", res)
}
```

`全局变量`

```
package main

import "fmt"
//f1就是全局匿名函数
var (
	f1 = func(n1, n2 int) int {
		return n1 * n2
	}
)

func test() int {
	return f1(10, 10)
}
func main() {
	res := f1(20, 20)
	fmt.Printf("res结果：%d\n", res)

	res2 := test()
	fmt.Printf("res2结果：%d\n", res2)
}

```

# 5.4 Go 闭包

闭包(closure)：是由一个函数和其相关的引用环境组合的一个整体。（闭包=函数+引用环境）

```
package main

import (
	"fmt"
)

//是由一个函数和其相关的引用环境组合的一个整体。（闭包=函数+引用环境）
//函数addUpper返回值是个函数
//返回值是匿名函数 func(int)int
func test() func(int) int {
	//定义一个局部变量
	n := 10
	//返回一个匿名函数
	return func(x int) int {
		n += x
		return n
	}

}

/*
addUpper函数返回了一个匿名函数，这个匿名函数又引用了函数外的变量n，因此匿名函数+n组成了一个整体，形成闭包
当调用f函数时，n仅仅被初始化一次，因此每次调用形成累计

*/

func main() {
	//调用addUpper函数，获取返回值
	f := test()
	//此时f是匿名函数，对其传参调用
	fmt.Println(f(50)) //10+50=60
	fmt.Println(f(20)) //60+20=80
	fmt.Println(f(20)) //80+20=100 同一个f对象，保留了n的值

	f1 := test()
	fmt.Println(f1(10))
}
```

闭包代码修改

```
package main

import (
	"fmt"
)

//是由一个函数和其相关的引用环境组合的一个整体。（闭包=函数+引用环境）
//函数addUpper返回值是个函数
//返回值是匿名函数 func(int)int
func test() func(int) int {
	//定义一个局部变量
	n := 10
	var str = "oldboy"
	//返回一个匿名函数
	return func(x int) int {
		n += x
		str += string(36) //36对应的
		fmt.Println("此时str值：", str)
		return n
	}

}

/*
addUpper函数返回了一个匿名函数，这个匿名函数又引用了函数外的变量n，因此匿名函数+n组成了一个整体，形成闭包
当调用f函数时，n仅仅被初始化一次，因此每次调用形成累计

*/

func main() {
	//调用addUpper函数，获取返回值
	f := test()
	//此时f是匿名函数，对其传参调用
	fmt.Println(f(50)) //10+50=60
	fmt.Println(f(20)) //60+20=80
	fmt.Println(f(20)) //80+20=100 同一个f对象，保留了n的值

	//新的初始化
	f1 := test()
	fmt.Println(f1(10))
}
```

# 闭包实战

```
package main

import (
	"fmt"
	"strings"
)

/*
1.makeSuffixFunc函数接收一个文件名后缀，如.png，且返回闭包
2.调用闭包，传入文件名前缀，如果没有后缀就添加后缀，返回 文件名.png
3.strings.HasSuffix可以判断指定字符串后缀
*/

func makeSuffixFunc(suffix string) func(string) string {
	//返回值闭包函数
	return func(filename string) string {
		//如果没有xx后缀，执行代码
		if !strings.HasSuffix(filename, suffix) {
			//则字符串拼接
			return filename + suffix
		}
		//否则有后缀名，则直接返回新文件名
		return filename
	}
}

func main() {
	//f1返回的是闭包函数，对此闭包函数进行功能性使用
	f1 := makeSuffixFunc(".png")

	fmt.Println(f1("苍老师"))  //没有后缀
	fmt.Println("小泽老师.png") //有后缀
}

```

总结：

```
1.makeSuffixFunc函数中的变量suffix和返回值匿名函数，组合成了一个闭包
2.由于闭包函数保留了上次引用的值suffix，只需要传入一次，即可反复使用
```

# 5.5 Go defer

程序开发中经常要创建资源（数据库初始化连接，文件句柄，锁等），在程序执行完毕都必须得释放资源，Go提供了defer（延时机制）更方便、更及时的释放资源。

```
1.内置关键字defer 用于延迟调用
2.defer在return前执行，常用于资源释放
3.多个defer按	先进后出	的机制执行
4.defer语句的变量，在defer声明时定义
```

实例

```
package main

import (
	"fmt"
)

func testDefer1() {
	//defer机制 先入后出，如同羽毛球筒
	defer fmt.Println("hello v1") //顺序5
	defer fmt.Println("hello v2") //顺序4
	defer fmt.Println("hello v3") //顺序3
	fmt.Println("aaaaa")          // 顺序1
	fmt.Println("bbbb")           //顺序2
}

func testDefer2() {

	for i := 0; i < 5; i++ {
		//每次循环，defer将后入的语句压到defer栈
		//依旧先入后出
		defer fmt.Printf("i=%d\n", i)
	}

	fmt.Printf("running\n") //顺序1
	fmt.Printf("return\n")  //顺序2
}

func testDefer3() {
	var i int = 0
	//defer是声明时定义好的，之后再修改无效，因此i=0
	defer fmt.Printf("defer i=%d\n", i)
	i = 1000
	fmt.Printf("i=%d\n", i)
}

func main() {
	//testDefer1()
	//testDefer2()
	testDefer3()
}
```

# 5.6 Go 常用函数

最正确的学习模块姿势：

```
https://golang.org/pkg/		//golang官网
```

程序开发常用函数

strings处理字符串相关

```
统计字符串长度，按字节				   len(str)
字符串遍历,处理中文					r:=[]rune(str)
字符串转整数		 			      n, err := strconv.Atoi("12")
整数转字符串 						  str = strconv.Itoa(12345)
字符串 转 []byte				   var bytes = []byte("hello go")
[]byte 转 字符串				   str = string([]byte{97, 98, 99})
10 进制转 2, 8, 16 进制:			  str = strconv.FormatInt(123, 2) // 2-> 8 , 16
查找子串是否在指定的字符串中		 	strings.Contains("seafood", "foo") //true
统计一个字符串有几个指定的子串 		strings.Count("ceheese", "e") //4
不区分大小写的字符串比较(==是区分字母大小写的)  fmt.Println(strings.EqualFold("abc", "Abc")) // true
返回子串在字符串第一次出现的 index 值，如果没有返回-1 	 strings.Index("NLT_abc", "abc") // 4
返回子串在字符串最后一次出现的 index，如没有返回-1 		strings.LastIndex("go golang", "go")
将指定的子串替换成 另外一个子串 strings.Replace("go go hello", "go", "go 语言", n) ，n 可以指 定你希望替换几个，如果 n=-1 表示全部替换
按照指定的某个字符，为分割标识，将一个字符串拆分成字符串数组  strings.Split("hello,wrold,ok", ",")
将字符串的字母进行大小写的转换: strings.ToLower("Go") // go strings.ToUpper("Go") // GO
将字符串左右两边的空格去掉: strings.TrimSpace(" tn a lone gopher ntrn ")
将字符串左右两边指定的字符去掉 : strings.Trim("! hello! ", " !") 
将字符串左边指定的字符去掉 : strings.TrimLeft("! hello! ", " !")
将字符串右边指定的字符去掉 :strings.TrimRight("! hello! ", " !")
判断字符串是否以指定的字符串开头: strings.HasPrefix("ftp://192.168.10.1", "ftp") 
判断字符串是否以指定的字符串结束: strings.HasSuffix("NLT_abc.jpg", "abc") //false
```

## 时间日期函数

日期时间相关函数经常用到

```
package time
//time包提供了时间的显示和测量用的函数，日历计算用的是公历
```

time包用法

```
package main

import (
	"fmt"
	"time"
)

func main() {
	//获取当前时间
	now := time.Now()
	fmt.Printf("现在时间：%v\n", now)
	fmt.Printf("现在时间类型%T\n", now)
	//通过now获取年月日 时分秒
	fmt.Printf("现在时间 年=%v 月=%v 日=%v 时=%v 分=%v 秒=%v\n", now.Year(), int(now.Month()), now.Day(), now.Hour(), now.Minute(), now.Second())

	//时间格式化,这个时间固定2006-01-02 15:04:05 必须这么写
	fmt.Printf(now.Format("2006-01-02 15:04:05\n"))

	//Unix时间戳和UnixNano用法
	fmt.Printf("unix时间戳=%v unixnano时间戳=%v\n", now.Unix(), now.UnixNano())
}
```

计算程序执行时间

```
package main

import (
	"fmt"
	"strconv"
	"time"
)

//计算程序运行时间
func test() {
	str := ""
	for i := 0; i < 100000; i++ {
		//将int转为string
		str += "oldboy" + strconv.Itoa(i)
	}
}

func main() {
	//程序开始前的时间戳
	start := time.Now().Unix()
	test()
	//程序结束时的时间戳
	end := time.Now().Unix()
	fmt.Printf("执行test()函数，花费时间%v秒\n", end-start)
}
```

# 5.7 Go 捕获异常

Go语言处理异常不同于其他语言处理异常的方式。

```
传统语言处理异常：
try 
catch
finally
```

go语言

```
引入了defer、panic、recover
1.Go程序抛出一个panic异常，在defer中通过recover捕获异常，然后处理
```

# defer与recover捕获异常

```
package main

import "fmt"

func test() {
	//在函数退出前，执行defer
	//捕捉异常后，程序不会异常退出
	defer func() {
		err := recover() //内置函数，可以捕捉到函数异常
		if err != nil {
			//这里是打印错误，还可以进行报警处理，例如微信，邮箱通知
			fmt.Println("err错误信息：", err)
		}
	}()

	//如果没有异常捕获，直接报错panic，运行时出错
	num1 := 10
	num2 := 0
	res := num1 / num2
	fmt.Println("res结果：", res)

}

func main() {
	test()
	fmt.Println("如果程序没退出，就走我这里")
}
```

# 5.8 Go 单元测试

如果你不想后半生的美好时光都在寻找BUG中度过，那么必须写些程序用来检测产品代码的结果和预期的一样。

Go语言的测试依赖于go test测试命令和一组按约定方式编写的测试函数，测试命令可以运行这些测试函数。

Go单元测试对文件名和方法名有严格的要求。

```
1、文件名必须以xx_test.go命名
2、方法必须是Test[^a-z]开头
3、方法参数必须 t *testing.T
4、使用go test执行单元测试
```

go test是go自带的测试工具，其中包含单元测试和性能测试

```
通过go help test可以看到go test的使用说明：

格式形如：
go test [-c] [-i] [build flags] [packages] [flags for test binary]

参数解读：
-c : 编译go test成为可执行的二进制文件，但是不运行测试。

-i : 安装测试包依赖的package，但是不运行测试。

关于build flags，调用go help build，这些是编译运行过程中需要使用到的参数，一般设置为空

关于packages，调用go help packages，这些是关于包的管理，一般设置为空

关于flags for test binary，调用go help testflag，这些是go test过程中经常使用到的参数

-test.v : 是否输出全部的单元测试用例（不管成功或者失败），默认没有加上，所以只输出失败的单元测试用例。

-test.run pattern: 只跑哪些单元测试用例

-test.bench patten: 只跑那些性能测试用例

-test.benchmem : 是否在性能测试的时候输出内存情况

-test.benchtime t : 性能测试运行的时间，默认是1s

-test.cpuprofile cpu.out : 是否输出cpu性能分析文件

-test.memprofile mem.out : 是否输出内存性能分析文件

-test.blockprofile block.out : 是否输出内部goroutine阻塞的性能分析文件

-test.memprofilerate n : 内存性能分析的时候有一个分配了多少的时候才打点记录的问题。这个参数就是设置打点的内存分配间隔，也就是profile中一个sample代表的内存大小。默认是设置为512 * 1024的。如果你将它设置为1，则每分配一个内存块就会在profile中有个打点，那么生成的profile的sample就会非常多。如果你设置为0，那就是不做打点了。

你可以通过设置memprofilerate=1和GOGC=off来关闭内存回收，并且对每个内存块的分配进行观察。

-test.blockprofilerate n: 基本同上，控制的是goroutine阻塞时候打点的纳秒数。默认不设置就相当于-test.blockprofilerate=1，每一纳秒都打点记录一下

-test.parallel n : 性能测试的程序并行cpu数，默认等于GOMAXPROCS。

-test.timeout t : 如果测试用例运行时间超过t，则抛出panic

-test.cpu 1,2,4 : 程序运行在哪些CPU上面，使用二进制的1所在位代表，和nginx的nginx_worker_cpu_affinity是一个道理

-test.short : 将那些运行时间较长的测试用例运行时间缩短
```

目录结构

```
test
	  |
	   —— calc.go
	  |
	   —— calc_test.go
```

calc.go

```
package main

func add(a, b int) int {
    return a + b
}

func sub(a, b int) int {
    return a - b
}
```

calc_test.go

```
package main

import (
    "testing"
)

func TestAdd(t *testing.T) {
    r := add(2, 4)
    if r != 6 {
        t.Fatalf("add(2, 4) error, expect:%d, actual:%d", 6, r)
    }
    t.Logf("test add succ")
}
```

输出结果：

```
cd test/
ls
calc.go		calc_test.go

//-v参数显示通过函数的信息
yugoMBP:test yuchao$ go test -v
=== RUN   TestAdd
--- PASS: TestAdd (0.00s)
        calc_test.go:11: test add succ...is ok
PASS
ok      gostudy/gobook/test     0.006s

```

单元测试文件代码规则：

```
1.文件名必须是_test.go结尾的，这样在执行go test的时候才会执行到相应的代码
2.你必须import testing这个包
3.所有的测试用例函数必须是Test开头
4.测试用例会按照源代码中写的顺序依次执行
5.测试函数TestXxx()的参数是testing.T，我们可以使用该类型来记录错误或者是测试状态
6.测试格式：func TestXxx (t *testing.T),Xxx部分可以为任意的字母数字的组合，但是首字母不能是小写字母[a-z]，例如Testintdiv是错误的函数名。
7.函数中通过调用testing.T的Error, Errorf, FailNow, Fatal, FatalIf方法，说明测试不通过，调用Log方法用来记录测试的信息。
```