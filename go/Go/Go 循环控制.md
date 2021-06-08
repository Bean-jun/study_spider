# Go if-else

Golang程序的流程控制决定程序如何执行，主要有三大流程控制，`顺序控制`、`分支控制`、`循环控制`。

条件语句需要定义一个或多个条件，并且对条件测试的true或false来决定是否执行。

## 顺序控制

代码自上而下逐行执行，中间没有判断、跳转，按默认流程执行，即顺序控制。

## 分支控制

让程序有选择的执行，有`单分支`、`双分支`、`多分支`

**单分支**

语法

```
if 表达式为真{
    //代码
}else{
    //否则进入此语句块
}
```

实例

```
package main

import "fmt"

func main() {
	var age int
	fmt.Println("请输入您的年纪：")
	//获取用户输入,传入变量地址，防止值拷贝
	fmt.Scanln(&age)
	if age > 18 {
		fmt.Println("你已经是个18岁的小伙子了！！加油")
	}
}
```

多重if嵌套

```
package main

import "fmt"

func main() {
	a := 100
	b := 200
	if a == 100 {
		if b == 200 {
			fmt.Println("a为100,b为200")
		}
	} else {
		fmt.Println("a或b有一个不匹配")
	}

}
```

**双分支**

```
package main

import "fmt"

func main() {
	var age int
	fmt.Println("请输入您的年纪：")
	//获取用户输入,传入变量地址，防止值拷贝
	fmt.Scanln(&age)
	if age > 18 {
		fmt.Println("你已经是超过18岁的小伙子了！！加油")
		//这个else不能换行，必须这么写
	} else {
		fmt.Println("未满18，回家写作业！！")
	}
}
```

**多分支**

![](/media/uploads/2019/03/_book/Chapter4/pic/1.png)

```
package main

import (
	"fmt"
)

/*
有一核桃，将被进行以下处理
干干巴巴、麻麻赖赖、那就盘他！！
通透圆润，好东西！！
甭管什么东西，盘他！！

*/
func main() {
	var hetao string
	fmt.Println("请输入核桃的成色")
	fmt.Scanln(&hetao) //写入变量

	//多分支判断
	if hetao == "干干巴巴，麻麻赖赖" {
		fmt.Println("盘他！！")
	} else if hetao == "通透圆润" {
		fmt.Println("好东西！！")
	} else {
		fmt.Println("管他三七二十，来啥盘啥!!")
	}
}
```

# 4.2 Go switch

switch语句用于基于不同条件执行不同动作，每一个case分支唯一，自上而下逐一测试，直到匹配结束，默认`自动终止`，`不需要break`。

# switch基本语法

1. switch后面跟着表达式（变量、常量、有返回值函数等）
2. case后面的表达式必须和switch表达式数据类型一致
3. case后可以有多个表达式
4. case后面表达式常量不得重复

```
package main

import "fmt"

func main() {
	var week int
	fmt.Println("请输入星期几:")
	fmt.Scanln(&week)

	switch week {
	case 1:
		fmt.Println("星期一，上班！！")
	case 2, 3, 4, 5:
		fmt.Println("星期二到星期五，你还得上班！！")
	case 6:
		fmt.Println("周六你就想休息？加班！！")
	case 7:
		fmt.Println("老子迟早要辞职，终于能休息了！！")
	default:
		fmt.Println("输入错误你就必须得上班！！")
	}
}
```

5. switch替代if-else使用

```
package main

import "fmt"

func main() {
	var score int
	fmt.Println("请录入你的成绩:>")
	fmt.Scanln(&score)
	switch {
	case score > 90:
		fmt.Println("成绩优秀")
	case score >= 70:
		fmt.Println("及格中等")
	case score >= 60:
		fmt.Println("勉强及格了")
	default:
		fmt.Println("恭喜你，考试不及格")
	}
}
```

6. switch之穿透`fallthrough`，在case语句块后添加fallthrough会继续执行下一个case

```
package main

import "fmt"

func main() {
	var score int
	fmt.Println("请录入你的成绩:>")
	fmt.Scanln(&score)
	switch {
	case score > 90:
		fmt.Println("成绩优秀")
		fallthrough
	case score >= 70:
		fmt.Println("及格中等")
	case score >= 60:
		fmt.Println("勉强及格了")
	default:
		fmt.Println("恭喜你，考试不及格")
	}
}
```

7.switch还可以用于判断interface变量实际存储的变量类型。

```
package main

import "fmt"

func main() {
	var x interface{} //x是空接口类型，可以接收任意类型
	var y = 19.9
	x = y
	switch i := x.(type) {
	case nil:
		fmt.Printf("x的类型是%T\n", i)
	case float64:
		fmt.Printf("x的类型是%T\n", i)
	default:
		fmt.Println("未知类型")
	}
}
```

## switch和if

判断的具体数值不多，符合整数、浮点数、字符、字符串等类型，建议用switch。

对bool类型的判断，用if，if可控范围更广。


# 4.3 Go for

Go的for循环是一个循环控制结构，可以执行循环次数。

语法

```
package main

import "fmt"

func main() {
	//创建方式一,循环条件是布尔值表达式
	num := 0
	for num <= 10 {
		fmt.Println("我说老男孩golang 你说哟", num)
		num++
	}

	//创建方式二,无限循环，go不存在while语法
	num1 := 0
	for {
		if num1 <= 10 {
			fmt.Println("人生苦短 说go就go", num1)
		} else {
			break //超出了就终止这个for循环
		}
		num1++ //等于num1=num1+1
	}
	
	fmt.Println("----------")
	//创建方式三  for-range  用于遍历字符串、数组
	var teacher = "wu pei qi"
	//字符串可以用索引取值，注意格式化输出的时候，要输出码值对应的字符  %c 格式化
	for i := 0; i < len(teacher); i++ {
		fmt.Printf("%c\n", teacher[i])
	}
	fmt.Println("----------")
	
	//创建方式四
	student := "chaoge牛逼"
	//for range遍历，是按照字符方式遍历，支持中文
	for k, v := range student {
		fmt.Printf("索引：%v 值：%c\n", k, v)
	}
	fmt.Println("----------")
	//传统遍历字符串是按字节遍历，汉字对应utf8编码是3个字节
	var class1 string = "python全栈开发班"
	//必须转化为[]rune切片类型，方可使用
	class2 := []rune(class1)
	for i := 0; i < len(class2); i++ {
		fmt.Printf("%c\n", class2[i])
	}
}
```

打印乘法表，层数由用户输入

```
package main

import "fmt"

func main() {
	var num int
	fmt.Println("请输入层数：")
	fmt.Scanln(&num)
	//i表示层数
	for i := 1; i <= num; i++ {
		//j表示每层打印多少
		for j := 0; j <= i; j++ {
			fmt.Printf("%v * %v = %v \t", j, i, j*i)
		}
		fmt.Println()
	}
}
```

三次登录

```
package main

import "fmt"

func main() {
	var name string
	var pwd string
	var logincache = 3
	//循环限制三次登录
	for i := 1; i <= 3; i++ {
		fmt.Println("请输入账号：")
		fmt.Scanln(&name)
		fmt.Println("请输入密码：")
		fmt.Scanln(&pwd)
		if name == "alex" && pwd == "alex3714" {
			fmt.Println("欢迎鸡汤王归来！！")
			break
		} else {
			logincache-- //每次登录失败减一
			fmt.Printf("你还有%v次机会尝试，老铁\n", logincache)
		}
	}
}
```

# 4.4 Go goto continue break

Go语言的goto语句可以无条件的跳转到指定的代码行执行。

goto语句一般与条件语句结合，实现条件转义，跳出循环体等。

Go程序`不推荐使用goto`，以免造成程序混乱，难以阅读。

实例：

```
package main

import "fmt"

func main() {
	var num int = 100

	fmt.Println("num值100")
	if num > 90 {
		goto label
		//此处代码已经不走，直接goto了
		fmt.Println("呵呵")
	}
	fmt.Println("我是占位符")
	fmt.Println("我是占位符")
	fmt.Println("我是占位符")
	fmt.Println("我是占位符")
	fmt.Println("我是占位符")
	//触发了goto，进入本次标签
label:
	fmt.Println("由于触发了goto，进入到我这里了")

	fmt.Println("我也是占位符")
	fmt.Println("我也是占位符")
	fmt.Println("我也是占位符")
}
```

## break

用于`中断当前循环`或`跳出switch中的case语句`

```
package main

import "fmt"

func main() {
	var num int = 10

	for num < 50 {
		fmt.Printf("a的值是：%v\n", num)
		num++
		if num > 30 {
			break //跳出for循环
		}
	}
}
```

**break label**

当处于多层嵌套for循环，直接跳出所有循环嵌套，可以用break label特性

```
package main

import (
	"fmt"
)

func main() {
	fmt.Println("主程序开始执行")
Exit:
	for i := 0; i < 9; i++ {
		for j := 0; j < 9; j++ {
			if i+j > 15 {
				fmt.Println("程序结束")
				break Exit
			}
		}
	}
	fmt.Println("已跳出循环体")
}
```

## continue语句

continue语句跳出当前循环剩余代码，继续进行下一次循环。

```
package main

import "fmt"

func main() {
	/* 定义局部变量 */
	var a int = 10

	/* for 循环 */
	for a < 20 {
		if a == 15 {
			/* 当a等于15时，跳出循环，让a++，等于16，跳过本次循环 */
			a++
			continue
		}
		fmt.Printf("a 的值为 : %d\n", a)
		a++
	}
}
```

## return语句

return用在方法或函数中，表示终止所在的方法或函数(method与function)。

return在main函数中，表示终止main函数，终止程序。

```
package main

import "fmt"

func main() {
	for i := 0; i <= 10; i++ {
		if i == 5 {
			return //直接退出main函数了
		}
		fmt.Printf("本次循环次数：%d\n", i)
	}
	//永远走不带这里了，第五次for循环时候，直接return了
	fmt.Println("循环结束，走到了我")
}
```