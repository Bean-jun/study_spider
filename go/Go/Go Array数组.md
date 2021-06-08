# 3.8 Go Array数组

数组是`固定长度`的特定类型元素组成的`序列`。

一个数字由零或多个元素组成。

数组的长度是固定，因此Go更常用Slice（切片，动态增长或收缩序列）。

数组是值类型，用`索引`下标访问每个元素，范围是`0~len(数组)-1`，访问越界会panic异常

**赋值和传参是复制整个数组而不是指针**

```
package main

import (
	"fmt"
)

func main() {
	/*
		定义数组
		var 数组名 [数组大小]数据类型
		var a1 [5]int

		定义数组后，5个元素都有默认值 0

		数组赋值方式
		a[0]=1
		a[1]=2

		数组的第一个元素的地址，就是数组的首地址
		数组各个元素地址间隔根据数组的数据类型决定,int64 8字节  int32 4字节
	*/
	var intArr [5]int
	fmt.Println("intArr默认值是：", intArr)
	intArr[0] = 1
	intArr[1] = 2
	intArr[2] = 3
	fmt.Println("intArr赋值后的值是：", intArr)
	fmt.Printf("intArr数组地址是=%p\n", &intArr)
	fmt.Printf("intArr数组第一个元素地址是=%p\n", &intArr[0])
	fmt.Printf("intArr数组第二个元素地址是=%p\n", &intArr[1])
	fmt.Printf("intArr数组第三个元素地址是=%p\n", &intArr[2])

	//(全局声明)
	//声明赋值方式
	var a1 [5]string = [5]string{"大猫", "二狗"}
	//自动类型推导,未赋值的有默认值
	var a2 = [5]int{1, 2, 3}
	//自动判断数组长度
	var a3 = [...]int{1, 2, 3, 4, 5}
	//指定索引赋值元素
	var a4 = [...]string{3: "狗蛋", 6: "猫屎"}
	//结构体类型数组
	var a5 = [...]struct {
		name string
		age  int
	}{
		{"王麻子", 10},
		{"吕秀才", 29},
	}
	fmt.Println(a1)
	fmt.Println(a2)
	fmt.Println(a3)
	fmt.Println(a4)
	fmt.Println(a5)
}

```

运行结果

```
GOROOT=/usr/local/go #gosetup
GOPATH=/Users/yuchao/go #gosetup
/usr/local/go/bin/go build -o /private/var/folders/dd/1j1pbw895772hqp2d2gfg00c0000gn/T/___go_build_main_go /Users/yuchao/go/src/gostudy/gobook/main.go #gosetup
/private/var/folders/dd/1j1pbw895772hqp2d2gfg00c0000gn/T/___go_build_main_go #gosetup
intArr默认值是： [0 0 0 0 0]
intArr赋值后的值是： [1 2 3 0 0]
intArr数组地址是=0xc42001c090
intArr数组第一个元素地址是=0xc42001c090
intArr数组第二个元素地址是=0xc42001c098
intArr数组第三个元素地址是=0xc42001c0a0
[大猫 二狗   ]
[1 2 3 0 0]
[1 2 3 4 5]
[   狗蛋   猫屎]
[{王麻子 10} {吕秀才 29}]

Process finished with exit code 0

```

## 遍历数组

```
package main

import "fmt"

func main() {
	var a1 = [...]int{1, 2, 3, 4, 5, 6}
	//通过索引取值
	for i := 0; i < len(a1); i++ {
		fmt.Println(a1[i])
	}

	//for循环遍历数组，索引和值,index可以省略用占位符_
	for index, value := range a1 {
		fmt.Println(index, value)
	}

}
```

## 数组使用细节

```
package main

import "fmt"

func main() {
	//数组是多个相同类型数据的组合，且长度固定，无法扩容
	var a1 [3]int
	a1[0] = 1
	a1[1] = 11
	//必须赋值int类型数据，否则报错
	//a1[2] = 111.1

	//不得超出索引
	//a1[3]=111
	fmt.Println(a1)//有默认值[1 11 0]
}
```

数组使用步骤：

1. 声明数组
2. 给数组元素赋值
3. 使用数组
4. 数组索引从0开始，且不得越界否则panic
5. Go数组是值类型，变量传递默认是值传递，因此会进行值拷贝
6. 修改原本的数组，可以使用引用传递（指针）

```
package main

import (
	"fmt"
)

//函数接收值类型，默认有值拷贝
func test(arr [3]int) {
	arr[0] = 66
}

//函数修改原本数组，需要使用引用传递
func test2(arr *[3]int) {
	(*arr)[0] = 66 //可以缩写arr[0]=66 编译器自动识别,arr是指针类型
}

func main() {
	//声明arr数组，需要考虑传递函数参数时，数组的长度一致性
	arr := [3]int{11, 22, 33}
	//test函数不会修改数组
	test(arr)
	fmt.Println(arr)
	//test2修改了数组
	test2(&arr)
	fmt.Println(arr)
}
```