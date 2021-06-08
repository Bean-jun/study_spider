Go变量

变量是对内存中数据存储空间的表示，如同门牌号对应着房间，同样的，变量名字对应变量的值。

变量使用步骤

```
1.声明变量，定义变量
2.给与变量赋值
3.使用变量
```

实际案例

```
package main

import "fmt"

func main() {
	var name string               //声明变量名 name
	name = "超哥"                   //给与变量赋值
	fmt.Println("name的值是：", name) //使用变量
}

```

结果

```
name的值是： 超哥
```

变量使用过程

```
代码读取
变量加载到内存  name 指向 内存地址的值
1）变量含有名字，变量类型
```

### 变量定义方式

1）定义变量与类型，不赋值，含有默认值

语法：`var 语句定义变量的列表，类型在后面`，可以定义局部变量也可以，也可全局变量

`var name string`

`var age int`

声明多个变量

`var num,num2 int`

```
package main

import "fmt"

func main() {
	var age int
	fmt.Println("age的值是：", age)

	var name string
	fmt.Println("name的值是：", name)

	var salary float64
	fmt.Println("salary的值是：", salary)

}

```

结果

```
age的值是： 0
name的值是： 
salary的值是： 0
```

2）编译器类型推导，自行判断变量类型

`var num = 10.1`

一次性定义多个变量

`var age,age2 = 10,11`

```
package main

import "fmt"

func main() {
	var num, num1 = 10, 11
	fmt.Println(num, num1)
}

```

3）短声明，省略var，`只能用在函数内部`

```
package main

import "fmt"

func main() {
	name := "超哥"
	fmt.Println("name的值是：", name)

	//上述段声明等于如下方式
	var name2 string
	name2 = "超哥"
	fmt.Println(name2)
}
```

4）多变量声明

golang支持一次性声明多个变量

`多个局部变量`

作用域只在函数体内，参数和返回值也是局部变量

```
package main

import "fmt"

func main() {
	//一次性声明多个变量，int默认值
	var n1, n2, n3 int
	fmt.Println(n1, n2, n3)

	//声明多个变量，且赋值
	var c1, c2, c3 = "chaoge", 18, 99.99
	fmt.Println(c1, c2, c3)

	//短声明多个变量
	a1, a2, a3 := "yu", 17, 100.0
	fmt.Println(a1, a2, a3)
}
```

5）`一次性声明多个全局变量`

```
package main

import "fmt"
//声明全局变量方式1
var n1 = 100
var n2 = 200
var n3 = 300
//声明全局变量方式2
var (
	d1, d2, d3 = 1, 2, 3
)
//声明全局变量方式3
var (
	c1 = 100
	c2 = 200
	c3 = 300
)

func main() {
	fmt.Println("这里是函数体内")
}
```

6）特殊变量，占位符 "_"

```
package main

import "fmt"

func Person(a1 int, n1 string) (int, string) {
	return a1, n1
}

func main() {
	_, name := Person(18, "好嗨哦")
	fmt.Println(name)
}

```

7）常见数据类型变量默认值

```
package main

import "fmt"

func main() {
	// 只声明变量，不赋值，只有默认值
	var age int
	var name string
	var gender bool
	var salary float64
	fmt.Println("age默认值 :", age)
	fmt.Println("name默认值 :", name)
	fmt.Println("gender默认值 :", gender)
	fmt.Println("salary默认值 :", salary)
}

```

输出结果

```
age默认值 : 0
name默认值 : 
gender默认值 : false
salary默认值 : 0
```

# Go常量

常量代表只读的，不可修改的值，用const关键字定义。

如同用常量定义 "π"之类的常数。

常量如同变量一样，可以批量声明，或者一组相关的常量。

常量的计算都在编译期间完成，并非运行期间！减少运行时的工作。

未使用的常量不会引发编译错误。(这点和变量不一样哦~)

```
package main

import (
	"fmt"
	"unsafe"
)

//常量定义且赋值
const World string = "世界"

//多常量初始化
const x, y int = 1, 2

//常量类型推断，字符串类型
const s1 = "Hello golang"

//常量组
const (
	e       = 2.71828182845904523536028747135266249775724709369995957496696763
	pi      = 3.14159265358979323846264338327950288419716939937510582097494459
	b  bool = true
)

//常量组，可以除了第一个外其他的常量右边的初始化表达式可以省略
//如果省略初始化表达式，默认使用前面常量的表达式
//与上一个常量相同
const (
	c1=1
	c2
	c3
	c4="c44444"
	c5
)
/*
输出结果
1
1
1
c44444
c44444
 */

 //常量也可以定义函数的返回值
 const (
 	f1="abc"  //长度为3的字符串类型
 	f2=len(f1)//返回长度的函数结果
 	f3=unsafe.Sizeof(f2)//返回f2所占用的内存大小
 /*
 输出结果
 abc
 3
 8
  */

func main() {
	fmt.Println(f1)
	fmt.Println(f2)
	fmt.Println(f3)
}

```

# Go常量之iota常量生成器

iota用于生成一组相似规则初始化的常量，在const常量声明的语句中，第一个常量所在行，iota为0，之后每一个常量声明加一。

例如time包的例子，一周7天，每天可以定义为常量，1~6，周日为0，这种类型也称为枚举

```
package main

import (
	"fmt"
)

const (
	Sunday = iota
	Monday //通常省略后续行表达式
	Tuesday
	Wednesday
	Thursday
	Friday
	Saturday
)

func main() {
	fmt.Println(Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday)
}
```

如果iota表达式被打断，需要显示恢复

```
package main

import (
	"fmt"
)

const (
	A = iota //初始0
	B        // +1
	C = "c"  //iota枚举被打断 ，为  c
	D        // c，与上  相同。
	E = iota // 4，显式恢复。注意计数包含了 C、D 两个，此时为4 。
	F        // 恢复iota 加一，此时为5
)

func main() {
	fmt.Println(A, B, C, D, E, F)
}
```

输出结果

```
0 1 c c 4 5

```

# 3.2 Go整数类型

Go语言的数值类型包含不同大小的整数型、浮点数和负数，每种数值类型都有大小范围以及正负符号。

![](/media/uploads/2019/03/_book/Chapter3/pic/p2.png)

整型的使用

1. golang整数类型分为有符号和无符号
2. golang默认整型是int型

```
package main

import "fmt"

func main() {
	var n1 = 100
	fmt.Printf("n1的类型：%T \n", n1)
}
```

输出结果

```
n1的类型：int 
```

3. 查看变量的字节大小，和数据类型

```
package main

import (
	"fmt"
	"unsafe"
)

func main() {
	var n2 int64 = 100
	//unsafe包底下的Sizeof函数，返回变量占用字节数
	fmt.Printf("n2的类型是：%T，占用的字节数是%d", n2, unsafe.Sizeof(n2))
}
```

输出结果

```
n2的类型是：int64，占用的字节数是8
```

## 数字类型

| 序号 | 类型和描述                                                   |
| ---- | ------------------------------------------------------------ |
| 1    | **uint8** 无符号 8 位整型 (0 到 255)                         |
| 2    | **uint16** 无符号 16 位整型 (0 到 65535)                     |
| 3    | **uint32** 无符号 32 位整型 (0 到 4294967295)                |
| 4    | **uint64** 无符号 64 位整型 (0 到 18446744073709551615)      |
| 5    | **int8** 有符号 8 位整型 (-128 到 127)                       |
| 6    | **int16** 有符号 16 位整型 (-32768 到 32767)                 |
| 7    | **int32** 有符号 32 位整型 (-2147483648 到 2147483647)       |
| 8    | **int64** 有符号 64 位整型 (-9223372036854775808 到 9223372036854775807) |

# 3.3 Go浮点型

Go 语言提供了两种精度的浮点数，float32 和 float64，编译器默认声明为float64

小数类型就是存放小数的，如`1.2` `0.005` `-2.32`

```
package main

import "fmt"

func main() {
   var price float32 = 100.02
   fmt.Printf("price类型是：%T，值是%v", price, price)//%T 类型  %v 默认值
}
```

![](/media/uploads/2019/03/_book/Chapter3/pic/p3.png)

### 浮点数形式

```
浮点数=符号位+指数位+位数位
```

```
package main

import "fmt"

func main() {
	var price float32 = 11.22 //正数符号
	fmt.Println("price=", price)
	var num1 float32 = -3.4 //负数符号
	var num2 float64 = -8.23
	fmt.Println("num1=", num1, "num2=", num2)

	//尾数可能丢失，精度缺损
	var num3 float32 = -123.11111111105//精度丢失了	
	var num4 float64 = -123.11111111105//float64的精度高于float32
	fmt.Println("num3=", num3, "num4=", num4)
	//输出结果
	//num3= -123.111115 num4= -123.11111111105
}
```

# 3.4 Go字符型

Golang 中没有专门的`字符`类型，如果要存储单个`字符(字母)`，一般使用 **byte** 来保存。 

普通字符串就是一串固定长度的字符连接起来的字符序列。

**Go 的`字符串`是由单个`字节`连接起来的。**

也 就是说对于传统的`字符串`是由`字符`组成的，而 **Go** 的字符串不同，它是由字节组成的。 

Go的字符用`单引号`表示

Go的字符串用`双引号`表示

```
package main

import "fmt"

func main() {
	var c1 byte = 'a'
	var c2 byte = '2' //字符的2
	
	//直接输出byte的值，也就是输出对应的字符的码值
	fmt.Println("c1=", c1)
	fmt.Println("c2=", c2)
	
	//输出字符的值，需要格式化输出
	fmt.Printf("c1值=%c  c2值=%c\n", c1, c2)
}

```

Go变量保存的byte 对应码值ASCII表，范围在[0-1,a-z,A-Z...]

如果保存的字符对应码大于255，应该使用int而不是byte，否则overflows byte异常

```
var c3 int = '皮' //正确
var c4 byte = '皮' //overflows byte 报错
```

Go语言默认字符编码UTF-8，统一规定

Go字符的本质是一个整数，直接打印是UTF-8编码的码值

给与变量赋值整数，按%c格式化输出，得到的是unicode字符

```
var c4 int = 22269
fmt.Printf("c4=%c\n", c4)
//输出结果c4=国
```

Go语言允许使用转义符号"\"

Go语言字符类型允许计算，相当于整数运算，因为字符拥有对应的Unicode码

# 3.5 Go布尔型

一个布尔类型的值只有两种:true 和 false。

if 和 for 语句的条件部分都是布尔类型的值，并且==和
