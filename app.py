from flask import Flask, request, render_template
from datetime import datetime
from dateutil.relativedelta import relativedelta

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        birthdate = request.form['birthday']
        gender = request.form['gender']
        actural_retirement_month, base_retirement_month, months_until_target = calculate_retirement(birthdate, gender)
               
        return render_template('result.html', 
                                   actural_retirement_month=actural_retirement_month,
                                   base_retirement_month=base_retirement_month,
                                   months_until_target=months_until_target)
    return render_template('index.html')

def calculate_retirement(birthdate, gender):
    # 基础退休年龄（男性60岁，女性55岁）
    # 目标退休年龄（男性63岁，女性58岁） 
    base_retirement_age = 60 if gender == 'male' else 55
    # 目标退休年龄（男性63岁，女性58岁） 
    target_retirement_age = 63 if gender == 'male' else 58
      
    # 将生日转换为datetime对象  
    birthdate = datetime.strptime(birthdate, "%Y-%m-%d")  

    # 计算基础退休的月份
    base_retirement_month = datetime(birthdate.year + base_retirement_age, birthdate.month, 1)
    # 检查生效日期后剩余的月份
    new_rule_start_date = datetime(2025, 1, 1) 
    difference = relativedelta(base_retirement_month,new_rule_start_date)
    months_difference = difference.years * 12 + difference.months

    # 将 months_difference 转换为整数类型
    months_difference = int(months_difference)

    # 根据规则延长的月份数
    months_until_target = months_difference//4

    # 如果大于36，则设置为36
    months_until_target = min(months_until_target, 36)

    actual_retirement_date=base_retirement_month+relativedelta(months=months_until_target)

    # 对于已经退休人员，规则不变
    if actual_retirement_date < datetime.now():
        actual_retirement_date = base_retirement_month
    return actual_retirement_date.strftime("%Y-%m-%d"), base_retirement_month.strftime("%Y-%m-%d"), months_until_target


if __name__ == '__main__':
    # 启动应用
    app.run(debug=True)
