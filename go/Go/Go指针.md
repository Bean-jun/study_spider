# 3.7 Go指针

变量是一种方便的占位符，用于引用计算机内存地址。

```
1.指针默认值nil
2.通过&(取地值符)取变量地址
3.通过*(取值符)透过指针访问目标值
```

首先基本数据类型中，如`name="yugo"` ，变量`name`存的值是`yugo`

1）基本数据类型，变量存的是值，称为`值`类型

2）通过`&`符号获取变量的`地址`，例如`&name`

3）指针类型的变量，存的是`地址`，这个`地址`指向的空间存的是`值`

4）获取指针类型指向的`值`，使用`*`，例如`*ptr`，使用*ptr获取ptr指向的值

```
package main

import (
	"fmt"
)

func main() {
	var name string = "yugo"
	//查看name变量的内存地址，通过&name取地址
	fmt.Printf("name的内存地址：%v\n", &name)

	//指针变量，存的是内存地址
	//ptr指针变量指向变量name的内存地址
	var ptr *string = &name
	fmt.Printf("指针变量ptr的内存地址：%v\n", ptr)

	//获取指针变量的值，用*ptr
	//*ptr表示读取指针指向变量的值
	fmt.Printf("指针变量ptr指向的值是：%v\n", *ptr)
}

```

5）值类型（int、float、bool、string、array、struct）都有对应指针类型

比如`*int`和`*string`等等