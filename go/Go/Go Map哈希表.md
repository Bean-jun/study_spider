# 3.10 Go Map哈希表

map是key-value类型数据结构，读作（哈希表、字典），是一堆未排序的键值对集合。

map的key必须是支持相等运算符`==`、`!=`的类型，如int、bool、channel、string、pointer、array、sruct、interface。

通常map的key是int、string

map的value可以是任意类型，没有限制，通常是int、float、string、struct

# map声明

```
package main

import "fmt"

func main() {
	/*
		map声明语法
		var 变量名  map[keytype]valuetype

		var m1 map[string]string
		var m2 map[int]string
		var m3 map[int]map[string]string//map的value又是map

		注意map声明不会分配内存，必须make初始化才可以使用
	*/

	//声明map方式一
	//make函数可以合理申请一大块内存，避免后续扩张时性能问题
	var m1 map[string]string
	//标注map的初始容量为10
	m1 = make(map[string]string, 10)
	m1["一号"] = "大狗子"
	m1["二号"] = "二狗子"
	fmt.Println(m1)

	//声明方式二
	m2 := make(map[string]string)
	m2["男"] = "小黑"
	m2["女"] = "小女"
	fmt.Println(m2)

	//声明方式三
	m3 := map[string]string{
		"坦克": "德玛西亚",
		"射手": "伊泽瑞尔",
		"辅助": "星女",
	}
	m3["打野"] = "赵信"
	fmt.Println(m3)
}
```

# map增删改查

```
package main

import "fmt"

func main() {
	m1 := map[string]string{"k1": "v1", "k2": "v2"}
	fmt.Printf("m1值：%v\n", m1)

	//map插入值
	m1["k3"] = "v3"
	fmt.Printf("插入后m1值：%v\n", m1)

	//map修改值
	m1["k1"] = "v11111"
	fmt.Printf("修改k1值后：%v\n", m1)

	//map查找值
	val, ok := m1["k4"]
	if ok {
		fmt.Printf("k4的值是：%v\n", val)
	}

	//长度: 获取键值对数量
	m1Len := len(m1)
	fmt.Printf("m1长度：%v\n", m1Len)

	//判断key是否存在
	if val, ok := m1["k4"]; !ok {
		fmt.Printf("此key不存在\n")
	} else {
		fmt.Printf("此key的值：%v\n", val)
	}

	//删除map的key，如key不存在，delete不进行操作
	//delete函数按指定的键，将元素从映射中删除
	//一次性删除所有key可以遍历下，逐个删除
	//也可以重新make新map，让原本map被gc回收
	if _, ok := m1["k3"]; ok {
		delete(m1, "k3")
		fmt.Printf("已删除m1中的k3\n")
	} else {
		fmt.Printf("无法删除，此key不存在")
	}
	fmt.Printf("此时m1的值：%v\n", m1)
}

```

# map遍历

使用for-range结构遍历

```
package main

import "fmt"

func main() {
	//循环性生成10个key的map
	m1 := make(map[int]int)
	for i := 0; i < 10; i++ {
		m1[i] = i + 1
		fmt.Printf("m1的key：%v value:%v\n", i, m1[i])
	}
	fmt.Println(m1)
fmt.Println("--分割线--")
	//循环遍历map的值
	for k, v := range m1 {
		fmt.Printf("m1的key：%v m1的值%v\n", k, v)
	}
}
```

遍历复杂map

map的value又是map

```
package main

import "fmt"

func main() {
	//make初始化第一层map，分配内存
	stuMap := make(map[string]map[string]string)
	//第二层map初始化
	stuMap["stu01"] = make(map[string]string)
	stuMap["stu01"]["名字"] = "大狗子"
	stuMap["stu01"]["年纪"] = "18"

	//切记，map必须make后方可使用
	stuMap["stu02"] = make(map[string]string)
	stuMap["stu02"]["名字"] = "二麻子"
	stuMap["stu02"]["年纪"] = "17"

	fmt.Println(stuMap)

	//取出所有学生的信息
	for k, v := range stuMap {
		fmt.Printf("k值是学生：%v  v值是学生信息：%v\n", k, v)
		//k1是键，v1是值
		for k1, v1 := range v {
			fmt.Printf("\tk1：%v v1：%v\n", k1, v1)
		}
		fmt.Println()
	}
}
```

# map切片

声明一个切片(slice)，并且这个切片的类型是map，这就被称作slice of map，map切片，这样map的个数就可以`动态变化`了。

```
package main

import "fmt"

func main() {
	//声明map切片，
	// 默认值		[map[] map[] map[] map[] map[]]
	sliceMap := make([]map[string]string, 5)
	for i := 0; i < 5; i++ {
		//map必须初始化再用,遍历初始化
		sliceMap[i] = make(map[string]string)
	}
	sliceMap[0]["名字"] = "张飞"
	sliceMap[1]["性别"] = "不男不女"
	sliceMap[2]["体重"] = "三百斤"
	fmt.Println(sliceMap)
	fmt.Printf("容量：%v，长度：%v\n", cap(sliceMap), len(sliceMap))

	//动态扩容map切片，用append函数
	newSliceMap := map[string]string{
		"姓名": "狗子",
		"爱好": "吃包子",
	}
	//append函数进行切片扩容，动态增加
	sliceMap = append(sliceMap, newSliceMap)
	fmt.Println(sliceMap)
	fmt.Printf("容量：%v，长度：%v\n", cap(sliceMap), len(sliceMap))
}
```

# map排序

map默认是无序的，每次遍历都是不同的结果

```
package main

import "fmt"

func main() {
	//无须的map
	m1 := make(map[int]int)
	for i := 0; i < 10; i++ {
		m1[i] = i + 1
	}
	fmt.Println(m1)
}
```

golang没有针对map的key排序的方法。

必须先对key排序，然后根据key值就可以输出排序后的结果

```
package main

import (
	"fmt"
	"sort"
)

func main() {
	//定义一个m map变量
	m := map[string]string{"q": "q", "w": "w", "e": "e", "r": "r", "t": "t", "y": "y"}
	fmt.Println(m)
	//定义一个 string类型切片
	var slice []string
	//循环遍历map，取出所有的key和value
	for k, _ := range m {
		//循环将key添加到切片中
		slice = append(slice, k)
	}
	fmt.Printf("切片slice值 : %v\n", slice)
	//调用排序包，对切片进行排序，按照字母顺序排序
	sort.Strings(slice[:])
	fmt.Printf("排序后 切片slice值 : %v\n", slice)
	for _, v := range slice {
		fmt.Printf("排序后 m[%v]=%v\n", v, m[v])
	}
}
```

# map使用细节

1）map是引用类型，遵循引用类型传递的机制，在函数接收map参数，对map修改是直接操作原本的map。

```
package main

import "fmt"

func modify(m map[string]string) {
	m["名字"] = "狗子"

}
func main() {
	//map是引用类型，遵循引用引用类型传递
	m1 := make(map[string]string)
	m1["名字"] = "傻子"
	m1["年纪"] = "十八"
	fmt.Println(m1)
	modify(m1) //直接对m1进行修改，说明是引用类型
	fmt.Println(m1)
}
```

2）map可以自动扩容，动态增长。

```
package main

import "fmt"

func main() {
	//初始化m1，限制容量3
	m1 := make(map[int]int, 3)
	for i := 0; i < 10; i++ {
		m1[i] = i + i
	}
	fmt.Println(m1)
	fmt.Printf("m1元素个数：%v", len(m1))
}
```

3）map的value也可以是struct类型，适合更复杂的数据

```
package main

import "fmt"

type Stu struct {
	Name    string
	Age     int
	Address string
}

func main() {
	//map的value可以为更复杂的struct结构体类型
	//map的key是学号
	//map的value是结构体{姓名、年纪、住址}
	students := make(map[int]Stu, 10)
	//初始化结构体,不需要填写key，顺序value即可
	stu1 := Stu{"alex", 1000, "沙河"}
	stu2 := Stu{"武沛奇", 999, "于辛庄"}
	students[1] = stu1
	students[2] = stu2
	fmt.Println(students)
	//遍历map，取出学生信息
	for k, v := range students {
		fmt.Printf("学生编号%v\n", k)
		fmt.Printf("学生姓名%v\n", v.Name)
		fmt.Printf("学生年纪%v\n", v.Age)
		fmt.Printf("学生住址%v\n", v.Address)
		fmt.Println("--------")
	}
}
```