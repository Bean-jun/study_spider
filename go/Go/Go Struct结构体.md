# 3.11 Go Struct结构体

Golang支持OOP面向对象编程。

Go的结构体`struct`如同python的`class`。

Go基于struct实现OOP特性，只有组合`composition`这个特性。

# 结构体概念

1）将一类事务特性提取出一个新的数据类型，就是结构体。

2）通过结构体可以创建多个实例。

3）可以是Student结构体、可以是Animal、Person结构体。

# 结构体特点

1）struct用于定义复杂数据结构

2）struct可以包含多个字段

3）struct可以定义方法（注意不是函数，是golang的method）

4）struct可以是值类型

5）struct类型可以嵌套

6）Go没有class，只有stuct类型

7）结构体是自定义类型，不得与其他类型强转

8）可以为struct每一个字段添加tag，这个tag可以反射机制获取，场景如json序列化和反序列化。

# 结构体定义

```
package main

import "fmt"

type Person struct {
	Name string
	Age  int
}
func main() {
	//声明方式
	p1 := Person{"小黑", 18} //有序赋值，并且必须包含所有字段，否则报错
	p2 := Person{Age: 18}  //关键词赋值，未赋值字段有空值
	fmt.Println(p1)
	fmt.Println(p2)
}
```

练习struct

```
package main

import "fmt"

//声明结构体名称Stu
type Stu struct {
	Name    string //结构体字段
	Age     int    //如未赋值有默认空值
	Address string
	Score   int
}

//结构体可以定义复杂的类型
type Person struct {
	Name  string
	Age   int
	Score [5]float64        //容量为5的数组
	prt   *int              //指针类型
	slice []int             //int类型切片
	map1  map[string]string //map类型字段
	//slice和map默认值是nil，必须make初始化才可使用
}

//结构体是值类型，不同结构体实例之间互不影响
type Monster struct {
	Name string
	Age  int
}

func main() {
	//声明结构体类型变量
	var stu1 Stu
	//结构体可以通过 . 的方式赋值，声明赋值方式一
	stu1.Name = "小黑"
	stu1.Age = 18
	stu1.Address = "沙河"
	stu1.Score = 100
	fmt.Printf("stu1的名字=%v 年纪=%v 住址=%v 分数=%v\n", stu1.Name, stu1.Age, stu1.Address, stu1.Score)

	//声明赋值方式二
	monster1 := Monster{"红孩儿", 18}
	monster2 := Monster{"女妖怪", 999}
	//两个结构体实例，内存地址不一样，确保独立
	fmt.Printf("monster1地址：%p\n", &monster1)
	fmt.Printf("monster2地址：%p\n", &monster2)

	//声明方式三
	//用来分配内存，主要用来分配值类型，比如int、struct。返回指向类型的 指针
	//此时m1是一个指针
	var m1 *Monster = new(Monster)
	//给m1赋值
	(*m1).Name = "孙悟空" //编译器自动识别 同于 m1.Name="孙悟空"
	(*m1).Age = 9999   //同上
	fmt.Println(*m1)   //此时m1是指针变量，加上*取值

	//声明方式四
	m2 := &Monster{
		"猪八戒",
		888,
	}
	fmt.Println(*m2)
	//第三、第四种返回结构体指针,go编译器自动识别，简化程序员心智负担，建议用1、2方法
}
```

# 结构体细节

1. 结构体字段在内存中是连续的

```
package main

import "fmt"

type Test struct {
	A int32
	B int32
	C int32
	D int32
}

func main() {
	var t Test
	fmt.Printf("a addr:%p\n", &t.A)
	fmt.Printf("b addr:%p\n", &t.B)
	fmt.Printf("c addr:%p\n", &t.C)
	fmt.Printf("d addr:%p\n", &t.D)
}
```

1. 结构体由用户自定义，可以类型转换，但必须完全相同字段、个数、类型
2. 对结构体进行重新定义（重新type），效果同于结构体`别名`
3. struct每个字段，可以写一个tag，这个tab可以通过反射获取，用在序列化，反序列化

```
package main

import (
	"encoding/json"
	"fmt"
)

type User struct {
	UserName string  `json:"姓名"` //反引号括起来的就是struct tag
	Sex      string  `json:"性别"`
	Score    float32 `json:"成绩"`
	Age      int32   `json:"年纪"`
}

func main() {
	user := &User{
		UserName: "user01",
		Sex:      "男",
		Score:    99.2,
		Age:      18,
	}
	//将user变量序列化为json格式字符串
	data, _ := json.Marshal(user)
	fmt.Printf("json str:%s\n", string(data))
}

```

## 结构体内存分配

先看代码

```
package main

import "fmt"

type Person struct {
	Name string
	Age  int
}

func main() {
	//p1有自己的结构体内存地址，
	var p1 Person
	p1.Age = 10
	p1.Name = "王大锤"

	//定义P2 指针类型，指向p1的内存地址
	var p2 *Person = &p1
	//两种形式一样，go编译器自动识别
	fmt.Println((*p2).Age)
	fmt.Println(p2.Age)
	//修改p2的结构体值，也就是修改了p1的结构体值
	p2.Name = "葫芦娃"
	fmt.Printf("输出结果  p2.Name=%v p1.Name=%v\n", p2.Name, p1.Name)
	fmt.Printf("输出结果(*p2).Name=%v p1.Name=%v\n", (*p2).Name, p1.Name)

	//查看p1和p2的内存地址
	fmt.Printf("p1内存地址%p\n", &p1)
	//p2是指针变量，自己也有一块内存地址，p2的值指向
	fmt.Printf("p2内存地址%p p2的值是%v\n", &p2, p2)
}
```

## 结构体内存分布原理图
![](/media/uploads/2019/03/_book/Chapter3/pic/p8.jpg)