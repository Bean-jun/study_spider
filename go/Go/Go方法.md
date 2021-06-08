# 第六章 Go方法

在[第三章](../Chapter3/11.md)中讲解了struct，面向对象编程OOP已经是一个编程范式了，Go语言同样支持OOP开发。

一个对象就是一个变量，在这个对象中包含了一些方法，一个方法是一个和特殊类型关联的函数。

一个Person结构体，除了有基本的字段（姓名、年纪、性别…等等），Person结构体还应该有一些行为动作，如（吃饭、说话、跑步、学习等…），这些事需要定义`方法`去完成。

Go的方法是作用在`指定的数据类型`上的，与数据类型绑定，`自定义类型`都可以有方法，不仅仅是struct。隐式的将struct实例作为第一实参（receiver）。

## 方法的声明和调用

```
package main

import "fmt"

//定义一个结构体数据类型
type Person struct {
	Username string
	Age      int
	Sex      string
}

//表示给Person结构体，绑定添加test方法
func (p Person) test() {
	fmt.Println("通过p变量，取出结构体类型中的Username值是：", p.Username)
}

func main() {
	p1 := &Person{
		"狗子",
		18,
		"男",
	}
	p1.test()
}
```

总结method

```
1.test方法和Person结构体类型绑定
2.test方法只能通过Person结构体的实例调用
```

语法

```
一个方法就是一个包含了接受者的函数，接受者可以是命名类型或者结构体类型的一个值或者是一个指针。

所有给定类型的方法属于该类型的方法集。

方法定义：

func (recevier type) methodName(参数列表)(返回值列表){}

参数和返回值可以省略
package main

type Test struct{}

// 无参数、无返回值
func (t Test) method0() {

}

// 单参数、无返回值
func (t Test) method1(i int) {

}

// 多参数、无返回值
func (t Test) method2(x, y int) {

}

// 无参数、单返回值
func (t Test) method3() (i int) {
	return
}

// 多参数、多返回值
func (t Test) method4(x, y int) (z int, err error) {
	return
}

// 无参数、无返回值
func (t *Test) method5() {

}

// 单参数、无返回值
func (t *Test) method6(i int) {

}

// 多参数、无返回值
func (t *Test) method7(x, y int) {

}

// 无参数、单返回值
func (t *Test) method8() (i int) {
	return
}

// 多参数、多返回值
func (t *Test) method9(x, y int) (z int, err error) {
	return
}

func main() {}
```

自定义数据类型绑定方法

```
package main

import (
	"fmt"
)

type Integer int

func (i Integer) Print() {
	fmt.Println("i的值：", i)
}

func main() {
	var a Integer
	a = 1000
	a.Print()

	var b int = 200
	a = Integer(b)
	a.Print()
}
```

## 方法实战

```
package main

import "fmt"

//定义一个结构体数据类型
type Person struct {
	Username string
	Age      int
	Sex      string
}

//此时这个(p Person)就是一个接受者
//Person结构体，人是可以说话的，添加speak方法
func (p Person) speak() {
	fmt.Printf("大声的喊出了自己的名字:%v\n", p.Username)
}

//人还可以蹦跳
func (p Person) jump() {
	fmt.Printf("%v:跳起来一拳打在了姚明的膝盖上\n", p.Username)
}

//人还可以进行算数
//方法的参数列表与返回值列表，与函数一致
func (p Person) getSum(n1, n2 int) int {
	sum := n1 + n2
	fmt.Printf("%v:飞快的计算出%d+%d的结果是%d\n", p.Username, n1, n2, sum)
	return sum
}
func main() {
	p1 := &Person{
		"李二狗",
		18,
		"男",
	}
	p1.speak()
	p1.jump()
	res := p1.getSum(1, 2)
	fmt.Printf("p1.getSum方法返回值是%d\n", res)
}
```

## 方法使用细节

1）结构体类型是值类型，在方法调用中，遵守值类型的传递机制，是值拷贝传递方式

2）如程序员希望在方法中，修改结构体变量的值，可以通过结构体指针的方式来处理

3）当接受者不是一个指针时，该方法操作对应接受者的值的副本(意思就是即使你使用了指针调用函数，但是函数的接受者是值类型，所以函数内部操作还是对副本的操作，而不是指针操作。

```
package main

import "fmt"

type People struct {
	Name    string
	Country string
}

//此方法进行了值拷贝
func (p People) Print() {
	fmt.Printf("我是谁:name=%s country=%s\n", p.Name, p.Country)
}

//此方法进行了值拷贝，不会对p1进行修改
func (p People) Set(name string, country string) {
	p.Name = name
	p.Country = country
}

//接收一个指针变量，可以修改原值
func (p *People) SetV2(name string, country string) {
	p.Country = country
	p.Name = name
}

func main() {
	var p1 People = People{
		Name:    "二狗子",
		Country: "沙河",
	}

	p1.Print()
	//此处修改无效，并没有修改p1的原地址
	p1.Set("二狗腿子", "日本")
	p1.Print()

	//两者效果一样，是被编译器进行了优化
	//(&p1).SetV2("people02", "english")
	p1.SetV2("狗官", "日本")
	p1.Print()
}
```

## 方法和函数的区别

1.调用方式区别

```
函数调用：	函数名(参数列表)
方法调用：	变量名.方法名(参数列表)
```

2.对于普通`函数`，接受者为`值类型`时，不能将`指针`类型数据直接传递，传递时编译器就提示报错

```
package main

import "fmt"

func test(n1 int) int {
	n1 = n1 + 10
	return n1
}

func test2(n1 *int) int {
	*n1 = *n1 + 10
	return *n1
}

func main() {
	var num = 10
	//test函数接收的num有一个值拷贝的过程
	res := test(num)
	fmt.Println("值传递函数test结果：", res)
	fmt.Println("值传递函数test修改num的结果:", num)
	
	//test2函数接收num变量的地址，因此修改的也是num的值
	res1 := test2(&num)
	fmt.Println("指针传递函数test2结果：", res1)
	fmt.Println("值传递函数test2修改num的结果:", num)
}
```

3.对于方法（如struct的方法），接受者是`值类型`时，可以直接用`指针类型`变量调用方法，反之亦然。

```
package main

import "fmt"

type Person struct {
	Name string
}

func (p Person) test01() {
	p.Name = "码云"
	fmt.Printf("test01修改了name值：%v\n", p.Name)
}

func (p *Person) test02() {
	p.Name = "麻花藤"
	fmt.Printf("test02修改了name值:%v\n", p.Name)
}

func main() {
	var p1 Person = Person{
		"刘强东",
	}
	fmt.Println("p1默认值:", p1)

	//调用test01,由于值拷贝，并没有修改默认p1的Name值
	//(&p1).test01() 即使传入地址，仍然进行了值拷贝
	p1.test01()
	fmt.Printf("此时main程序调用p1.test01，此时p1.Name值：%v\n", p1.Name)

	//传入地址
	//可以简写p1.test02()，修改的是p1.Name原本内存地址
	(&p1).test02()
	fmt.Printf("main程序调用p1.test02，此时p1.Name值%v\n", p1.Name)
}
```

# 6.2 Go 匿名字段

Golang匿名字段：可以像访问字段成员那样，访问匿名字段方法，go编译器自动查找。

```
package main

import "fmt"

type Student struct {
	id   int
	name string
}

type Teacher struct {
	//匿名字段
	Student
}

func (s1 *Student) Play() {
	fmt.Printf("Student地址：%p,值是%v\n", s1, s1)
	fmt.Println("我是个学生，但是我就爱玩儿，你能奈我何")
}
func main() {
	t1 := &Teacher{Student{1, "银角大王吧"}}
	//两种方式一样效果
	/*
		t1 := &Teacher{
			Student{
				1,
				"银角大王吧",
			},
		}
	*/
	fmt.Printf("t1的内存地址：%p\n", &t1)
	//通过t1变量，执行结构体Student的方法，查找
	t1.Play() //  t1 -> Teacher -> *Student
}
```

通过匿名字段可以实现

`重写 override`

## Go继承实战

写一个学生管理系统，学生类别有(小学生、中学生、大学生)，既然是学生群体都可以（查询成绩、设置成绩）

```
package main

import "fmt"

//学生结构体
type Student struct {
	Name  string
	Age   int
	Score int
}

//显示学生个人信息方法，接收指针类型
func (stu *Student) ShowInfo() {
	fmt.Printf("学生姓名：%v 年龄=%d 成绩=%d\n", stu.Name, stu.Age, stu.Score)
}

//设置学生成绩
func (stu *Student) SetScore(score int) {
	stu.Score = score
}

//小学生群体 单词pupil
type Pupil struct {
	//小学生的属性完全可以继承Student学生的属性
	Student //继承匿名字段
}

//小学生独有方法
func (p *Pupil) testing() {
	fmt.Println("小学生正在考试中..")
}

//大学生结构体，同样的也有学生的常见属性
type Graduate struct {
	Student
}

//大学生独有的方法
func (g *Graduate) testing() {
	fmt.Println("大学生正在答辩考试中...")
}

func main() {
	p1 := &Pupil{Student{"小学生一号", 7, 99}}
	p1.testing()
	p1.ShowInfo()
	p1.SetScore(100)
	p1.ShowInfo()
	fmt.Println("-----------")
	g1 := &Graduate{Student{"大学生一号", 22, 50}}
	g1.testing()
	g1.ShowInfo()
	g1.SetScore(60)
	g1.ShowInfo()
}
```

继承给Go程序带来了`代码的复用性`提高了，代码的可维护性、扩展性更高了！

注意点：

```
如果一个struct嵌套了另一个匿名结构体，那么这个结构可以直接访问匿名结构体的方法，从而实现继承
如果一个struct嵌套了另一个【有名】的结构体，那么这个模式叫做组合
```