## 7.1 Go interface

Go语言的主要设计者之一罗布·派克（Rob Pike）曾经说过，如果只能选择一个Go语言的特 性移植到其他语言中，他会选择`接口`。

接口在Go语言有着至关重要的地位。如果说`goroutine`和`channel `是支撑起Go语言的`并发模型` 的基石，让Go语言在如今`集群化`与`多核化`的时代成为一道极为亮丽的风景，那么`接口`是Go语言 整个`类型系统`的基石，让Go语言在基础编程哲学的探索上达到前所未有的高度。

Go语言在编程哲学上是变革派，而不是改良派。这不是因为Go语言有goroutine和channel， 而更重要的是因为Go语言的类型系统，更是因为`Go语言的接口`。Go语言的编程哲学因为有`接口` 而趋近完美。

```
接口只有方法声明，没有实现，也没有数据字段。
接口可以匿名嵌入到其他接口。
对象赋值给接口时，会发生拷贝。
只有当接口存储的类型和对象都是nil时，接口等于nil。
空接口可以接收任意的数据类型。
一个类型可以实现多个接口。
接口变量名习惯以 er 结尾。
```

------

```
接口类型是对其它类型行为的抽象和概括，接口类型不会和特定的实现细节绑定。
Go接口独特在它是隐式实现的，这是指：一个结构体只要实现了接口要求的所有方法，我们就说这个结构体实现了该接口。
```

------

`接口`在现实世界也是有真实场景的，如同笔记本上都有USB插口，且不用担心这个插槽是为`手机`、`U盘`、`平板`哪一个准备的，因为笔记本的usb插槽和各种设备的厂家统一了USB的插槽规范。

------

## 接口语法

```
type 接口名 interface {
    method1(参数列表)返回值列表
    method2(参数列表)返回值列表
}

interface类型可以定义一组方法，且不需要实现这些方法！并且interface不能有任何变量。
只要有一个变量类型，含有接口中的所有方法，就说这个变量类型实现了这个接口。
```

**Go多态与接口**

```
package main

import "fmt"

//定义一个Usb接口，且定义Usb功能方法
type Usb interface {
	Start()
	Stop()
}

type Phone struct {
	Name  string
	Price int
}

//让手机Phone实现Usb接口的方法
func (p Phone) Start() {
	fmt.Println("手机已连接USB,开始工作")
}

//必须实现接口所有的方法，少一个都报错  如下：Phone does not implement Usb (missing Stop method)
func (p Phone) Stop() {
	fmt.Println("手机断开了USB，停止工作")
}

type IPad struct {
	Name  string
	Price int
}

func (p IPad) Start() {
	fmt.Println("ipad已经连接USB，开始工作")
}

func (p IPad) Stop() {
	fmt.Println("ipad断开了USB，停止工作")
}

//定义一个电脑结构体，这个结构体可以实现usb的接口
type Computer struct {
}

//定义working方法，接收Usb接口类型变量
//实现Usb接口声明的所有方法
//这是一个多态的函数，调用同一个Working函数，不同的执行结果
func (mbp Computer) Working(usb Usb) {
	//不同的usb实参，实现不同的功能
	//只要实现了usb接口的数据类型，那么这个类型的变量，就可以给usb接口变量赋值
	usb.Start()
	usb.Stop()
}

func main() {
	//分别创建结构体对象
	c := Computer{}
	p := Phone{"苹果手机", 6999}
	i := IPad{"华为平板", 7999} 
	
	//
	//手机连接笔记本，插上手机
	c.Working(p)
	fmt.Printf("名字:%v 价格:%d\n", p.Name, p.Price)

	fmt.Println("------------------")
	//平板连接笔记本，插上平板
	c.Working(i)
	fmt.Printf("名字：%v 价格：%d\n", i.Name, i.Price)
}
```

接口实例2

```
package main

import "fmt"

//员工接口
type Employer interface {
	CalcSalary() float32
}

//开发者
type Programer struct {
	name  string
	base  float32
	extra float32
}

//创建开发者实例
func NewProgramer(name string, base float32, extra float32) Programer {
	return Programer{
		name,
		base,
		extra,
	}
}

//计算开发者工资，实现了CalcSalary方法
func (p Programer) CalcSalary() float32 {
	return p.base
}

//销售群体
type Sale struct {
	name  string
	base  float32
	extra float32
}

//创建销售实例
func NewSale(name string, base float32, extra float32) Sale {
	return Sale{
		name,
		base,
		extra,
	}
}

//实现了CalcSalary方法
func (p Sale) CalcSalary() float32 {
	return p.base + p.extra*p.base*0.5
}

//计算所有人的工资接收参数，接口切片
func calcAll(e []Employer) float32 {
	/*
		fmt.Println(e)
		[{码云 50000 0} {刘抢东 40000 0} {麻花藤 30000 0} {格格 3000 2.5} {小雪 1800 2.5} {小雨 2000 2.5}]
	*/
	var cost float32
	//忽略索引，v是每一个结构体
	for _, v := range e {
		cost = cost + v.CalcSalary()
	}
	return cost
}
func main() {
	p1 := NewProgramer("码云", 50000.0, 0)
	p2 := NewProgramer("刘抢东", 40000, 0)
	p3 := NewProgramer("麻花藤", 30000, 0)

	s1 := NewSale("格格", 3000, 2.5)
	s2 := NewSale("小雪", 1800, 2.5)
	s3 := NewSale("小雨", 2000, 2.5)

	var employList []Employer
	employList = append(employList, p1)
	employList = append(employList, p2)
	employList = append(employList, p3)
	employList = append(employList, s1)
	employList = append(employList, s2)
	employList = append(employList, s3)

	cost := calcAll(employList)
	fmt.Printf("这个月人力成本：%f\n", cost)
}
```



## Go接口细节

```
1.接口本身不能创建实例，但是可以指向一个实现了该接口的变量实例，如结构体
2.接口中所有方法都没有方法体，是没有实现的方法
3.Go中不仅是struct可以实现接口，自定义类型也可以实现接口，如type myInt int 自定义类型
4.一个自定义类型，只有实现了某个接口，才可以将自定义类型的实例变量，赋给接口类型，否则报错missing xx method
5.一个自定义类型，可以实现多个接口(实现多个接口的所有方法)
6.接口类型不得写入任何变量 如
type Usb interface{
    method1()
    method2()
    Name string  //错误，编译器不通过
}
7.接口A可以继承多个别的接口B、接口C，想要实现A，也必须实现B、C所有方法，称作接口组合
8.interface类型，默认是指针(引用类型)，如果没初始直接使用，输出nil，可以赋给实现了接口的变量
9.空接口interface{}，没有任何类型，也就是实现了任何类型，可以吧任何一个变量赋给空接口
10.匿名组合的接口，不可以有同名方法，否则报错duplicate method
```

# 7.2 Go type assertion

类型断言是使用在`接口值`上的操作。

语法`x.(T)`被称为类型断言，x代表接口的类型，T代表一个类型检查。

类型断言检查`它操作对象的动态类型`是否和`断言类型匹配`。

**类型断言快速入门**

```
package main

import (
	"fmt"
)

type Point struct {
	x int
	y int
}

func main() {

	var a interface{}
	var point Point = Point{1, 2}
	//任何类型都实现了空接口
	a = point
	fmt.Printf("类型：%T 值：%v\n", a, a)

	/*
		想要将a赋值给b变量，可以直接这么玩吗？
		var b Point
		b = a
		报错
		cannot use a (type interface {}) as type Point in assignment: need type assertion
		提示需要类型断言type assertion
	*/
	var b Point
	b, ok := a.(Point)
	if ok {
		fmt.Printf("类型：%T 值：%v\n", b, b)
	}
}
```

## 类型断言介绍

在类型断言时，如果类型不匹配，程序会直接panic异常退出，因此要确保类型断言，空接口指向的就是断言的类型，或者加上检查机制，防止程序panic退出。

```
package main

import (
	"fmt"
)

//test函数接收一个空接口，可以接收任意的数据类型
func test(a interface{}) {

	//带有检查机制的类型断言，ok是布尔值，返回true或false
	s, ok := a.(int)
	if ok {
		fmt.Println(s)
		//手动return结束这个类型检查
		return
	}

	str, ok := a.(string)
	if ok {
		fmt.Println(str)
		return
	}

	f, ok := a.(float32)
	if ok {
		fmt.Println(f)
		return
	}

	fmt.Println("can not define the type of a")
}

//测试test函数类型检查
func testInterface1() {
	var a int = 100
	test(a)

	var b string = "hello"
	test(b)
}

//使用分支判断，检测类型断言
func testSwitch(a interface{}) {
	//直接switch跟着类型断言表达式
	switch a.(type) {
	case string:
		fmt.Printf("a is string, value:%v\n", a.(string))
	case int:
		fmt.Printf("a is int, value:%v\n", a.(int))
	case int32:
		fmt.Printf("a is int, value:%v\n", a.(int))
	default:
		fmt.Println("not support type\n")
	}
}

func testSwitch2(a interface{}) {
	//将类型断言结果赋值给变量
	switch v := a.(type) {
	case string:
		fmt.Printf("a is string, value:%v\n", v)
	case int:
		fmt.Printf("a is int, value:%v\n", v)
	case int32:
		fmt.Printf("a is int, value:%v\n", v)
	default:
		fmt.Println("not support type\n")
	}
}

func testInterface2() {
	var a int = 123456
	testSwitch(a)
	fmt.Println("-------------")
	var b string = "hello"
	testSwitch(b)
}

func testInterface3() {
	var a int = 100
	testSwitch2(a)
	var b string = "hello"
	testSwitch2(b)
}

func main() {
	//testInterface1()
	//testInterface2()
	testInterface3()
}
```