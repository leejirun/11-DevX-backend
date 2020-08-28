import os
import django
import csv
import sys
import pandas as pd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'devx.settings')
django.setup()

from product.models	import *
from ast 		import literal_eval

CSV_PATH = './spaceX_edited.csv'
data = pd.read_csv(CSV_PATH,
    converters={
        "색깔"   :literal_eval,
        "사이즈" :literal_eval,
        "이미지" :literal_eval
    })
for _, row in data.iterrows() :
    main_c	= row[0]
    sub_c	= row[1]
    prod_name	= row[2]
    prod_price	= row[3][1:]
    prod_color	= row[4]
    prod_img	= row[5]
    prod_size	= row[6]
    prod_sizechart = literal_eval(row[7]) #2차원 리스트는 직접 list_eval을 걸어줘야 한다.
    #CSV에서 한 줄씩 불러와서 저장
    
    # 저장순서 : 카테고리 -> 서브카테고리 -> 상품 -> 색깔/상품-색깔 중간테이블 
    # -> 사이즈/상품-사이즈 중간테이블 -> 사이즈차트/상품-사이즈차트 중간테이블 -> 이미지
    
    cate, created	= Category.objects.get_or_create(name=main_c)
    subcate, created	= SubCategory.objects.get_or_create(name=sub_c, category=cate)
    #데이터가 입력된 테이블에서 객체 불러오는 변수 생성(카테고리 서브카테고리 색깔 )
    prod = Product.objects.create(
        name		=	prod_name,
        price		=	prod_price,
        sub_category	=	subcate
        )        
    #상품 데이터입력 / 객체를 변수에 저장
    for p_color in prod_color :
        color, created = Color.objects.get_or_create(name=p_color)
        ProductColor.objects.create(
            color=color,
            product=prod
        )
    for p_size in prod_size :
        size, created	= Size.objects.get_or_create(name=p_size)
        ProductSize.objects.create(
            size	= size,
            product	= prod
        )
    SizeChart.objects.create(table=prod_sizechart, product=prod)
    Image.objects.create(image=prod_img, product=prod)
   
        
