// arduino HT1621驱动 pdc0173 PDC-TD0173 by epro.taobao.com

// Pin 13 has an LED connected on most Arduino boards.
// give it a name:
int led = 13;
//HT1621驱动 pdc0173 PDC-TD0173
int CS =7 ;
int WR = 6;
int DATA =5 ;
int GND = 4;
int VCC = 3;
//#define sbi(x, y)  (x |= (1 << y))
//#define cbi(x, y)  (x &= ~(1 <<y ))
//#define  ComMode    0x52  //0x52 4COM,1/3bias  1000    010 1001  0   0x48 //0b1000 0100 1000 1/2duty 3com
//#define  RCosc      0x30  //内部RC振荡器(上电默认)1000 0011 0000
//#define  LCD_on     0x06  //打开LCD 偏压发生器1000     0000 0 11 0
//#define  LCD_off    0x04  //关闭LCD显示
//#define  Sys_en     0x02  //系统振荡器开 1000   0000 0010
//#define  CTRl_cmd   0x80  //写控制命令
//#define  Data_cmd   0xa0  //写数据命令
//#define WDTDIS      0X0A  //0b1000 0000 1010  禁止看门狗
//#define SYSDIS      0X00  //0b1000 0000 0000  关振系统荡器和LCD偏压发生器
//

//HT1621指令
#define  BIAS     0x52             //0b1000 0101 0010  1/3duty 4com
#define  SYSDIS   0X00             //0b1000 0000 0000  关振系统荡器和LCD偏压发生器
#define  SYSEN    0X02             //0b1000 0000 0010 打开系统振荡器
#define  LCDOFF   0X04             //0b1000 0000 0100  关LCD偏压
#define  LCDON    0X06             //0b1000 0000 0110  打开LCD偏压
#define  XTAL     0x28             //0b1000 0010 1000 外部接时钟
#define  RC256    0X30             //0b1000 0011 0000  内部时钟
#define  WDTDIS1  0X0A            //0b1000 0000 1010  禁止看门狗


#define WR0       digitalWrite(WR,LOW)   //拉低
#define WR1     digitalWrite(WR,HIGH)    //拉高
#define CS0     digitalWrite(CS,LOW)  //拉低
#define CS1     digitalWrite(CS,HIGH)  //拉高
#define DATA1    digitalWrite(DATA,HIGH)     //数据位
#define DATA0    digitalWrite(DATA,LOW)      //数据位


//定义要显示的值
unsigned int counter=7777;
unsigned int tmp;
unsigned int n1, n2, n3, n4;
unsigned char Ht1621Tab[]={0x00,0x00,0x00,0x00};

//                         0    1    2    3    4    5    6    7    8    9    三   A     B     C    D    E    F
unsigned char DispTab[]={0xEB,0x0A,0xAD,0x8F,0x4E,0xC7,0xE7,0x8A,0xEF,0xCF,0x85,0xEE, 0x67, 0xE1,0x2F,0xE5,0xE4};


 boolean ledFlog = false;
// the setup routine runs once when you press reset:
void setup() {               
  // initialize the digital pin as an output.
  pinMode(led, OUTPUT);   
  pinMode(CS,OUTPUT); 
  pinMode(WR,OUTPUT); 
  pinMode(DATA,OUTPUT);
  pinMode(VCC,INPUT);
  pinMode(GND,INPUT);


  delay(10);
  Ht1621_Init();        //上电初始化LCD
  delay(100);           //延时一段时间
  Ht1621WrAllData(0,Ht1621Tab,16);// Clear LCD display
  data_convertor(1150);
  Display();
  Display_lcd_dot();
}
// the loop routine runs over and over again forever:
void loop() {

   delay(1000);
   ledFlog = !ledFlog;
   if(ledFlog)
   {
     digitalWrite(led,HIGH);      //数据位
   }else{
     digitalWrite(led,LOW);      //数据位
   }

}
// Name: Init_1621(初始化1621)

void Ht1621_WR_1()
{
  WR1;
}
void Ht1621_WR_0()
{
  WR0;
}
void Ht1621_CS_0()
{
  CS0;
}
void Ht1621_CS_1()
{
  CS1;
}
void Ht1621_DAT_1()
{
  DATA1;
}
void Ht1621_DAT_0()
{
  DATA0;
}
/*******************************************************************************
****函数名称:
****函数功能:1621写数据函数
****版本:V1.0
****日期:14-2-2014
****入口参数:Data-要发送的数据  cnt-要发送的数据位数
****出口参数:
****说明:
********************************************************************************/
void Ht1621Wr_Data(unsigned char Data,unsigned char cnt)
{
  unsigned char i;
  for (i=0;i<cnt;i++)
   {
     Ht1621_WR_0();
     if((Data & 0x80)==0x80)
        {Ht1621_DAT_1();}
     else
        {Ht1621_DAT_0();}
     Ht1621_WR_1();
     Data<<=1;
   }
}
// Name: SendCmd(送命令)
/*******************************************************************************
****函数名称:
****函数功能:1621写指令函数
****版本:V1.0
****日期:14-2-2014
****入口参数:Cmd 命令
****出口参数:
****说明:
********************************************************************************/
void Ht1621WrCmd(unsigned char Cmd)
{
   Ht1621_CS_0();
   Ht1621Wr_Data(0x80,4);          //写入命令标志100
   Ht1621Wr_Data(Cmd,8);           //写入命令数据
   Ht1621_CS_1();
}

//Name: SendBit_1621(送数据程序)
/*******************************************************************************
****函数名称:
****函数功能:1621写一个数据函数
****版本:V1.0
****日期:14-2-2014
****入口参数:Addr--地址 Data--数据
****出口参数:
****说明:
********************************************************************************/
void Ht1621WrOneData(unsigned char Addr,unsigned char Data)
{
  Ht1621_CS_0();
  Ht1621Wr_Data(0xa0,3);  //写入数据标志101
  Ht1621Wr_Data(Addr<<2,6); //写入地址数据
  Ht1621Wr_Data(Data,4); //写入数据的前四位 7  6  5  4
  Ht1621_CS_1();
  delay(10);
} 


/*******************************************************************************
****函数名称:
****函数功能:1621写整屏数据函数
****版本:V1.0
****日期:14-2-2014
****入口参数:Addr--地址 p--数据  cnt数据个数
****出口参数:
****说明:
********************************************************************************/
void Ht1621WrAllData(unsigned char Addr,unsigned char *p,unsigned char cnt)
{
  unsigned char i;
  Ht1621_CS_0();
  Ht1621Wr_Data(0xa0,3); //写入数据标志101
  Ht1621Wr_Data(Addr<<2,6); //写入地址数据
  for (i=0;i<cnt;i++)
   {
    Ht1621Wr_Data(*p,8); //写入数据
    p++;
   }
  Ht1621_CS_1();
}

/*******************************************************************************
****函数名称:
****函数功能:1621初始化函数
****版本:V1.0
****日期:14-2-2014
****入口参数:
****出口参数:
****说明:
********************************************************************************/
void Ht1621_Init(void)
{
   Ht1621WrCmd(BIAS);
   Ht1621WrCmd(RC256);             //使用内部振荡器
   //Ht1621WrCmd(XTAL);             //使用外部振荡器
   Ht1621WrCmd(SYSDIS);
   Ht1621WrCmd(WDTDIS1);
   Ht1621WrCmd(SYSEN);
   Ht1621WrCmd(LCDON);
}
/*******************************************************************************
****函数名称:
****函数功能:1621显示函数
****版本:V1.0
****日期:14-2-2014
****入口参数:
****出口参数:
****说明:
********************************************************************************/
void Display(void)
{

   Ht1621WrOneData(0 , DispTab[n4]);
   Ht1621WrOneData(1 , DispTab[n4]<<4);

   Ht1621WrOneData(2 , DispTab[n3]);
   Ht1621WrOneData(3 , DispTab[n3]<<4);

   Ht1621WrOneData(4 , DispTab[n2]);
   Ht1621WrOneData(5 , DispTab[n2]<<4);

   Ht1621WrOneData(6 , DispTab[n1]);
   Ht1621WrOneData(7 , DispTab[n1]<<4);

}

/*******************************************************************************
****函数名称:
****函数功能:显示符号函数
****版本:V1.0
****日期:14-2-2014
****入口参数:Addr--地址 Data--数据
****出口参数:
****说明:
********************************************************************************/
void Display_lcd_dot(void)
{
  Ht1621WrOneData(0 , DispTab[n4]|0x10);//P1
   //Ht1621WrOneData(2 , DispTab[n3]|0x10);    //2P
   //Ht1621WrOneData(4 , DispTab[n2]|0x10);    //3P
   //Ht1621WrOneData(6 , DispTab[n1]|0x10);    //4P
}
/*******************************************************************************
****函数名称:
****函数功能:数据转换函数
****版本:V1.0
****日期:14-2-2014
****入口参数:adc_value-需要转换的数值
****出口参数:
****说明:
********************************************************************************/
void data_convertor(unsigned long adc_value)
{  
    tmp=adc_value;         //adc
    n4=tmp/1000;
    tmp=tmp%1000;
    n3=tmp/100;
    tmp=tmp%100;
    n2=tmp/10;
    tmp=tmp%10;
    n1=tmp;
 }
