'''
原始代码中，我们进行了循环穷举，然后比较计算结果。仔细征税办法的文档分析，对于年终奖拆入一个月的这种情况，年终奖不可能拆出超过50%，
因为年终奖是用商数来确定交税比例的，确定比例所用的表相当于月薪减去起征点。
当然还可以用数学进一步证明最大合理循环范围，基于这样分析，我们可以把循环的最大范围缩小一半。
计算优化：刚才我们把大问题分成了三部分，又把两个月的那种情况简化为相等的两个月，而两个相等的月进行税额计算的时候会用到只拆入一个月的那种情况下的数据，于是我们可以用空间来换时间。对拆入一个月计算的数据存入内存（list中），
在拆入两个月的时候只需要用的时候，用index去取就好了，这样一来，又会快很多。
同理，bonus_remain这个量也会被两部分复用，我们也放入内存中。
最后对拆入两月的情况继续缩小循环范围（年终的四分之一），我们可以得到改良代码如下：

'''
# coding=utf-8
import time

base_quota = 3500
tax_quota = [1500, 4500, 9000, 35000, 55000, 80000]
tax_rat = [0.03, 0.10, 0.20, 0.25, 0.30, 0.35, 0.45]
tax_quick = [0, 105, 555, 1005, 2755, 5505, 13505]
one_month = 0
two_month = 0

result = [0.0]
bonus_result = [0.0]
index_range = 0


# 相当于C里的main函数
def run():
    year_bonus = int(input('Please input bonus\n'))
    month_salary = int(input('Please input salary\n'))

    # 获取三种方案的税额（不拆分、拆入一个月、拆入两个月）
    start_time = round(time.clock(), 2)
    year_bonus_tax = get_only_bonus_tax(year_bonus, month_salary)
    one_month_tax = get_one_month_bonus(year_bonus, month_salary)
    two_month_tax = get_two_month_bonus(year_bonus, month_salary)

    # 取最小税额并计算税后奖金
    print("year_bonus_tax:", year_bonus_tax)
    print("one_month_tax:", one_month_tax)
    print("two_month_tax:", two_month_tax)
    # min_tax = min(year_bonus_tax, one_month_tax)
    min_tax = min(year_bonus_tax, one_month_tax, two_month_tax)
    bonus_remain = year_bonus - min_tax

    if min_tax == year_bonus_tax:
        print(year_bonus, "0", "0", bonus_remain)
    elif min_tax == one_month_tax:
        print(year_bonus - one_month, one_month, "0", bonus_remain)
    elif min_tax == two_month_tax:
        print(year_bonus - (two_month * 2), two_month, two_month, bonus_remain)
    else:
        return
    end_time = round(time.clock(), 2)
    print(u"耗时："),
    print (end_time - start_time)
    init()
    return


def init():
    global result, bonus_result, index_range
    result = [0.0]
    bonus_result = [0.0]
    index_range = 0
    run()


# 获取税率等级
def get_tax_num(money):
    for i in range(len(tax_quota)):
        if money > tax_quota[-1]:
            return len(tax_quota)
        elif money <= tax_quota[i]:
            return i
        else:
            continue


# 获取税率
def get_tax_rat(money):
    return rat(get_tax_num(money))


# 获取速算扣除数
def get_tax_quick(money):
    return quick(get_tax_num(money))


def rat(num):
    if num < len(tax_rat):
        return tax_rat[num]
    else:
        print("function rat error")


def quick(num):
    if num < len(tax_quick):
        return tax_quick[num]
    else:
        print("function quick error")


# 获取平常月交税金额
def get_month_tax(money):
    if money <= base_quota:
        return 0.0
    else:
        money -= base_quota
        return round(money * get_tax_rat(money) - get_tax_quick(money), 2)


# 获取年奖平均月交税金额
def get_per_month_tax(money):
    return money * get_tax_rat(money) - get_tax_quick(money)


# 获取不拆分年奖交税总额
def get_only_bonus_tax(year_bonus, month_salary):
    if month_salary <= base_quota:
        if year_bonus < base_quota - month_salary:
            tax = 0.0
        else:
            per_month = (year_bonus - (base_quota - month_salary)) / 12.0
            tax = (year_bonus - (base_quota - month_salary)) * get_tax_rat(per_month) - get_tax_quick(
                per_month)
    else:
        per_month = year_bonus / 12.0
        tax = round(year_bonus * get_tax_rat(per_month) - get_tax_quick(per_month), 2)

    return tax


def get_month_tax_add(month_salary, add_num):
    month_add_salary = month_salary + add_num
    month_tax_add = round(get_month_tax(month_add_salary) - get_month_tax(month_salary), 2)
    return month_tax_add


# 获取拆分为一个月交税总额
def get_one_month_bonus(year_bonus, month_salary):
    now_bonus_tax = get_only_bonus_tax(year_bonus, month_salary)
    half_bonus = int((year_bonus + 1) / 2) + 1
    global index_range
    index_range = half_bonus
    for i in range(1, half_bonus):
        bonus_remain = year_bonus - i
        month_tax_add = get_month_tax_add(month_salary, i)
        global result, bonus_result
        result.append(month_tax_add)
        bonus_result.append(get_only_bonus_tax(bonus_remain, month_salary))
        bonus_tax = round(bonus_result[-1] + month_tax_add, 2)
        # bonus_tax = round(get_only_bonus_tax(bonus_remain, month_salary) + month_tax_add, 2)

        if bonus_tax < now_bonus_tax:
            now_bonus_tax = bonus_tax
            global one_month
            one_month = i
    return now_bonus_tax


# 获取拆分为两个月交税总额
def get_two_month_bonus(year_bonus, month_salary):
    now_bonus_tax = get_only_bonus_tax(year_bonus, month_salary)
    quarter_bonus = int((index_range + 1) / 2)
    for i in range(1, quarter_bonus):
        # bonus_remain = year_bonus - (i * 2.0)
        month_tax_add = result[i] * 2.0
        # bonus_tax = round(get_only_bonus_tax(bonus_remain, month_salary) + month_tax_add, 2)
        bonus_tax = round(bonus_result[2 * i] + month_tax_add, 2)
        if bonus_tax < now_bonus_tax:
            now_bonus_tax = bonus_tax
            global two_month
            two_month = i
    return now_bonus_tax


# 运行主函数
run()

