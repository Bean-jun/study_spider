# 3.9 Go Slice切片

1. Go语言切片（Slice）
2. 切片是`可动态变化`的序列，是对数组的`引用`，`引用类型`，遵循引用传递的机制
3. slice类型写作[]T，T是slice元素类型，`var s1 []int`，s1就是切片变量

```
package main

import "fmt"

func main() {
   //创建一个数组
   var array1 [5]int = [...]int{11, 22, 33, 44, 55}
   /*
      创建切片，通过对数组的索引切片
      s1 是切片名
      array1[1:3]代表slice引用数组区间，索引1到索引3的值，注意取头不取尾，
   */
   s1 := array1[1:4]
   fmt.Println(array1)
   fmt.Println(s1)
   fmt.Println(len(s1))
   fmt.Println(cap(s1))
}
```

运行结果

```
[11 22 33 44 55] 	//原本数组
[22 33 44]			//切片的值
3					//切片元素长度
4					//切片容量
```

# 切片原理

slice是一个轻量级数据结构，提供访问数组子序列元素的功能。

slice由三个部分构成，指针、长度、容量

指针：指针指向slice`第一个元素`对应的`数组元素`的地址。

长度：slice元素的数量，不得超过容量。

容器：slice`开始的位置`到底层数据的`结尾`。

![](/media/uploads/2019/03/_book/Chapter3/pic/p6.jpg)

```
package main

import "fmt"

func main() {
//创建数组,Months月份，1月份到12月份
months:=[...]string{"","January","February","March","April","May","June","July","August","September","October","November","December"}
//创建切片，对数组的引用
s1:=months[4:7]//[April May June]
s2:=months[6:9]//[June July August]
fmt.Println(s1)
fmt.Println(s2)

//指针：指针指向slice`第一个元素`对应的`数组元素`的地址。
fmt.Printf("slice第一个元素地址%p\n",&s1[0])
fmt.Printf("对应数组元素的地址%p\n",&months[4])
}
```

对切片读写

```
package main

import (
	"fmt"
)

func main() {
	//创建数组data
	data := [...]int{0, 1, 2, 3, 4, 5}
	//切片s [2,3]
	s := data[2:4]
	//切片读写操作目标是底层数组data
	s[0] += 100
	s[1] += 200
	fmt.Println(s)
	fmt.Println(data)
}
```

运行结果

```
[102 203]
[0 1 102 203 4 5]
```

## 创建切片的方式

1. 定义切片，然后引用已经创建好的数组，数组可见
2. 内置make函数创建切片，底层数组看不见，只能通过slice访问元素

make创建切片内存分配图

![](/media/uploads/2019/03/_book/Chapter3/pic/p7.png)
```
package main

import (
"fmt"
)
/*
内置make函数，参数（类型，len，cap），注意cap大于len，容量可以省略，默认等于长度
切片有默认值
 */
var slice0 []int = make([]int, 10)
var slice1 = make([]int, 10)
var slice2 = make([]int, 10, 10)

func main() {
	fmt.Printf("make全局slice0 ：%v\n", slice0)
	fmt.Printf("make全局slice1 ：%v\n", slice1)
	fmt.Printf("make全局slice2 ：%v\n", slice2)
	fmt.Println("--------------------------------------")
	slice3 := make([]int, 10)
	slice4 := make([]int, 10)
	slice5 := make([]int, 10, 10)
	slice5[0] = 11
	slice5[1] = 22
	fmt.Printf("make局部slice3 ：%v\n", slice3)
	fmt.Printf("make局部slice4 ：%v\n", slice4)
	fmt.Printf("make局部slice5 ：%v\n", slice5)
}

```

3. 定义切片直接对应数组，如同make方式

```
package main

import "fmt"

func main() {
	//第三种方式，原理类似make，数组看不见，由make维护
	var s1 []int = []int{1, 2, 3, 4, 5}
	fmt.Println(s1)
	fmt.Println(len(s1))
	fmt.Println(cap(s1))
}
```

4.遍历切片

```
package main

import "fmt"

func main() {
	var arr [5]int = [...]int{11, 22, 33, 44, 55}
	s1 := arr[1:4]
	//for循环遍历
	for i := 0; i < len(s1); i++ {
		fmt.Printf("s1[%v]=%v\n", i, s1[i])
	}
	fmt.Println()

	//for range方式遍历切片
	for i, v := range s1 {
		fmt.Printf("索引i=%v 值v=%v\n", i, v)
	}
}
```

5.切片案例

```
package main

import "fmt"

func main() {
	var array1 = [...]int{11, 22, 33, 44}
	slice1 := array1[1:4] //11,22,33
	slice2 := array1[1:]  //22,33,44
	slice3 := array1[:]   //11,22,33,44
	slice4 := slice3[:2]   //slice4=[11,22] 切片再切片
	fmt.Println(slice1)
	fmt.Println(slice2)
	fmt.Println(slice3)
	fmt.Println(slice4)
}

```

6.cap是内置函数，统计切片容量，最大存放多少元素

7.切片扩容，append内置函数，向尾部添加数据，返回新的slice对象

```
package main

import "fmt"

func main() {
	//创建切片
	var slice1 []int = []int{100, 200, 300}
	fmt.Printf("slice1容量=%v 长度=%v\n", cap(slice1), len(slice1))
	//给切片追加新元素
	//容量扩容机制是2倍扩容
	slice1 = append(slice1, 400)
	fmt.Printf("slice1扩容后容量=%v 长度=%v\n", cap(slice1), len(slice1))
	fmt.Println(slice1)

	//切片扩容切片,slice1... 语法糖代表展开切片元素
	slice1=append(slice1,slice1...)
	fmt.Println(slice1)
}
/*
append原理就是对底层数组扩容，go会创建新的数组，将原本元素拷贝到新的数组中
slice重新引用新的数组
这个数组不可见
 */
```

8.切片拷贝

```
package main

import "fmt"

func main() {
	//创建切片
	var slice1 []int = []int{11, 22, 33, 44}
	//make创建切片,长度是10
	var slice2 = make([]int, 10)
	copy(slice2, slice1) //把slice1的值拷贝给slice2
	fmt.Println(slice1)  //[11 22 33 44]
	fmt.Println(slice2)  //[11 22 33 44 0 0 0 0 0 0]
	//slice1和slice2数据独立，互不影响
	slice1[0] = 123 
	fmt.Println(slice1)
	fmt.Println(slice2)
}
```

9.全切片表达式

array[x:y:z] 

切片内容 [x:y] 

切片长度: y-x 

切片容量:z-x

```
package main

import (
	"fmt"
)

//官网资料
// https://golang.google.cn/ref/spec#Slice_expressions
func main() {
	data := [...]int{0, 1, 2, 3, 4, 10: 0}
	s := data[1:2:3] //data[start:end:数字-start]  这个s容量是3-1=2
	fmt.Printf("s的容量是：%v\n", cap(s))
	s = append(s, 100, 200)         // 一次 append 两个值，超出 s.cap 限制。
	fmt.Println(s, data)            // 重新分配底层数组，与原数组无关。
	fmt.Printf("s的容量=%v\n", cap(s)) //二倍扩容
	fmt.Println(&s[0], &data[0])    // 比对底层数组起始指针。
}
```

# string和slice的联系

1）string底层就是byte数组，因此string同样可以进行切片处理

```
package main

import "fmt"

func main() {
	str1 := "yugo niubi"
	//对str1进行切片
	s1 := str1[:4]
	fmt.Println(s1)//yugo
}
```

2）string修改的两种方式

```
package main

import (
	"fmt"
)

func main() {
	str1 := "yugo niubi"
	//string是不可变的，也无法通过切片修改值
	//str1[0] = 's'  编译器失败

	//修改string的方法，需要string转化为[]byte，修改后转为string
	arr1 := []byte(str1) //类型强转
	arr1[0] = 'g'
	str1 = string(arr1)
	fmt.Printf("str1=%v\n", str1)

	//[]byte只能处理英文和数字，不能处理汉字，汉字3个字节，会出现乱码
	//将string转为[]rune，按字符处理，兼容汉字
	arr2 := []rune(str1)
	arr2[0] = '于'
	str1 = string(arr2)
	fmt.Printf("str1=%v\n", str1)
}
```