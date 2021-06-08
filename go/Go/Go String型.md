# 3.6 Go String型

字符串是一个不可改变的字节序列。

Go string通常是用来包含人类可读的文本。

文本字符串通常被解释为采用 UTF8 编码的 Unicode 码点。

Go的字符串由单个字节连接起来。

```
package main

func main() {
	var city string = "我爱北京天安门"
	println(city)
	// city[0]='1' 错误，go的字符串不可变
}
```

Go的字符串用双引号识别，识别转义字符"\n \t"

```
package main

import "fmt"

func main() {
	//识别转义符
	var story string = "妖怪\n放了我师父"
	fmt.Println(story)

	//反引号，以原生形式输出，包括特殊字符，防止注入攻击
	story2 := `
你看这个灯，它又大又亮
你好
我是银角大王吧，你吃了\n吗?
`
	fmt.Println(story2)
}
```

Go字符串拼接

```
package main

import "fmt"

func main() {
	//字符串拼接，识别空格
	str3 := "你好" + "  我是孙悟空"
	fmt.Println(str3)
}
```

Go可以用索引取出某字节

```
package main

import "fmt"

func main() {
	str3 := "hello world"
	//索引取出值的码值，格式化输出
	fmt.Printf("str3=%c\n",str3[1])
	//输出str3的长度
	fmt.Println(len(str3))
}
```

Go多行字符串拼接

```
package main

import "fmt"

func main() {
	//注意 +   加号 写在上一行
	myname := "wo" + "shi" + "bei" + "jing" +
		"sha" + "he" + "yu"
	fmt.Println(myname)
}
```

Go遍历字符串

```
package main

import "fmt"

func main() {
	myname := "hello world"
	for _, ret := range myname {
		fmt.Printf("ret=%c\n", ret)
	}
}
```

Go修改字符串的方法

```
package main

import "fmt"

func main() {
	myname := "hello world"
	m1 := []rune(myname) //转化为[]int32的切片,rune是int32的别名
	m1[4] = '皮'//修改索引对应的值
	myname = string(m1)//类型强转，rune转为string
	fmt.Println(myname)
}

```

## 字符串处理strings包

官网模块

https://golang.org/pkg/strings/

```
package main

import (
	"fmt"
	"strings"
)

func main() {
	str := "hello world"
	//判断是不是以某个字符串开头，返回布尔值
	res0 := strings.HasPrefix(str, "http://")
	res1 := strings.HasPrefix(str, "hello")
	fmt.Printf("res0 is %v\n", res0)
	fmt.Printf("res1 is %v\n", res1)

	//判断是不是以某个字符串结尾
	res3 := strings.HasSuffix(str, "http://")
	res4 := strings.HasSuffix(str, "world")
	fmt.Printf("res3 is %v\n", res3)
	fmt.Printf("res4 is %v\n", res4)

	//判断字符在字符串中首次出现的索引位置，没有返回-1
	res5 := strings.Index(str, "o")
	res6 := strings.Index(str, "x")
	fmt.Printf("res5 is %v\n", res5)
	fmt.Printf("res6 is %v\n", res6)

	//返回字符最后一次出现的索引位置，没有返回-1
	res7 := strings.LastIndex(str, "o")
	res8 := strings.LastIndex(str, "x")
	fmt.Printf("res7 is %v\n", res7)
	fmt.Printf("res8 is %v\n", res8)

	//字符串替换
	res9 := strings.Replace(str, "world", "golang", 2)
	res10 := strings.Replace(str, "world", "golang", 1)
	//trings.Replace("原字符串", "被替换的内容", "替换的内容", 替换次数)
	//原字符串中有2个world，才能替换2次
	fmt.Printf("res9 is %v\n", res9)
	fmt.Printf("res10 is %v\n", res10)

	//求字符在字符串中出现的次数，不存在返回0次
	countTime0 := strings.Count(str, "h")
	countTime1 := strings.Count(str, "x")
	fmt.Printf("countTime0 is %v\n", countTime0)
	fmt.Printf("countTime1 is %v\n", countTime1)

	//重复几次字符串
	res11 := strings.Repeat(str, 0)
	res12 := strings.Repeat(str, 1)
	res13 := strings.Repeat(str, 2)
	// strings.Repeat("原字符串", 重复次数)
	fmt.Printf("res11 is %v\n", res11)
	fmt.Printf("res12 is %v\n", res12)
	fmt.Printf("res13 is %v\n", res13)

	//字符串改大写
	res14 := strings.ToUpper(str)
	fmt.Printf("res14 is %v\n", res14)

	//字符串改小写
	res15 := strings.ToLower(str)
	fmt.Printf("res15 is %v\n", res15)

	//去除首尾的空格
	res16 := strings.TrimSpace(str)
	fmt.Printf("res16 is %v\n", res16)

	//去除首尾指定的字符,遍历l、d、e然后去除
	res17 := strings.Trim(str, "ld")
	fmt.Printf("res17 is %v\n", res17)

	//去除开头指定的字符
	res18 := strings.TrimLeft(str, "he")
	fmt.Printf("res18 is %v\n", res18)

	//去除结尾指定的字符,遍历d、l、r
	res19 := strings.TrimRight(str, "dlr")
	fmt.Printf("res19 is %v\n", res19)

	//用指定的字符串将string类型的切片元素结合
	str1 := []string{"hello", "world", "hello", "golang"}
	res20 := strings.Join(str1, "+")
	fmt.Printf("res20 is %v\n", res20)
}
```

# Go基本数据类型转化

Golang在不同的数据类型之间赋值时需要显示转化，无法自动转换。

语法：

```
T(v)  将v转化为T类型
T  数据类型 如 int32 int64 float32
V  需转化的变量
```

类型转化注意点：

1）Go中数据类型的转换可以从 数值范围大  >  数值范围小，反之也可，注意别`溢出`

2）被转化的变量存储的数值，变量本身的数据类型没变化

```
package main

import "fmt"

func main() {
	var num1 int32 = 100
	var num2 float32 = float32(num1)	//num2强转为浮点型
	fmt.Printf("num1=%v  num2=%v\n", num1, num2)	 //%v 值的默认格式
	fmt.Printf("num1类型是：%T", num1)//本身的类型 没有变化
}
```

3）不同类型变量之间的计算

```
package main

import "fmt"

func main() {
	var n1 int32 = 12
	var n2 int64 = 10

	//n3:=n1+n2 //不同类型之间无法计算,需要强转
	n3 := int64(n1) + n2
	fmt.Println(n3)
}
```

# Go基本数据类型与string转化

开发中经常将数据类型转成string

方法1：

**fmt.Sprintf("%参数",表达式)**

```
package main

import "fmt"

func main() {
	var num1 int = 66
	var num2 float64 = 25.25
	var b bool = true
	var myChar byte = 'c'
	
	//%q 单引号
	//%d 十进制表示
	str1 := fmt.Sprintf("%d", num1)
	fmt.Printf("str1 type %T str=%q\n", str1, str1)
	
	//%f 有小数点
	str2 := fmt.Sprintf("%f", num2)
	fmt.Printf("str2 type %T str2=%q\n", str2, str2)
	
	//%t 布尔值
	str3 := fmt.Sprintf("%t", b)
	fmt.Printf("str3 type %T str3=%q\n", str3, str3)
	
	//%c Unicode码对应的字符
	str4 := fmt.Sprintf("%c", myChar)
	fmt.Printf("str4 type %T str4=%q\n", str4, str4)
}
```

方法2：

**fmt.Strconv**

```
package main

import (
	"fmt"
	"strconv"
)

func main() {
	var num1 int = 99
	var num2 float64 = 66.66
	var b1 bool = true

	str1 := strconv.FormatInt(int64(num1), 10)
	fmt.Printf("str1类型是%T str1=%q\n", str1, str1)

	//参数解释
	// f 格式
	// 10 小数位保留10位
	// 64  表示float64
	str2 := strconv.FormatFloat(num2, 'f', 10, 64)
	fmt.Printf("str2类型是%T str2=%q\n", str2, str2)

	str3 := strconv.FormatBool(b1)
	fmt.Printf("str3类型是%T str3=%q\n", str3, str3)

	//Itoa，将int转为string
	var num3 int64 = 1123
	str4 := strconv.Itoa(int(num3))//必须强转int()
	fmt.Printf("str4类型是%T str4=%q\n", str4, str4)
}
```

### string类型转基本数据类型

![](/media/uploads/2019/03/_book/Chapter3/pic/p4.png)

官方函数介绍

**https://golang.org/pkg/strconv/**

```
package main

import (
	"fmt"
	"strconv"
)

func main() {
	/*
		ParseBool，ParseFloat，ParseInt和ParseUint将字符串转换为值
		如转换失败，返回新类型默认值
	*/
	var str1 string = "true"
	var b1 bool
	/*
		strconv.ParseBool(str1)函数返回2个值（value bool,err error)
	*/
	b1, _ = strconv.ParseBool(str1)
	fmt.Printf("b 值类型= %T  b值=%v\n", b1, b1)

	var str2 string = "1234"
	var num1 int64
	//func ParseInt（s string，base int，bitSize int）（i int64，err error）
	num1, _ = strconv.ParseInt(str2, 10, 64)
	fmt.Printf("num1类型：%T num2值：%v\n", num1, num1)

	var str3 string = "123.456"
	var float1 float64
	//func ParseFloat（s string，bitSize int）（float64，error）
	float1, _ = strconv.ParseFloat(str3, 64)
	fmt.Printf("float1类型：%T  float1值：%v", float1, float1)
}

```