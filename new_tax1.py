


# coding=utf-8
import time
base_quota = 3500
tax_quota = [1500, 4500, 9000, 35000, 55000, 80000]
tax_rat = [0.03, 0.10, 0.20, 0.25, 0.30, 0.35, 0.45]
tax_quick = [0, 105, 555, 1005, 2755, 5505, 13505]

one_month = 0
two_month = 0

'''
根据现有个人所得税计税办法，个人薪酬计税有两种方式，一种为月工资（含月奖金）计税，一种为年终奖综合计税。
在年终奖综合计税发放过程中，在某些区间会出现税前奖金增加，税后实际收入反而减少的情况。
为了合理避税，某公司计划拆分年终奖为综合计税发放和随月工资发放两种形式，随月工资发放次数最多为2个月。
设计一个年终奖自动拆分程序，输入为计税月工资额、应发年终奖，输出为综合计税应发年终奖、
第1个月随月工资发放奖金、第2个月随工资发放奖金。要求税后总收入最大，如税后收入相同，拆分发放次数约少越好。
1、拆分问题，年终奖最优拆分方案只会出现三种情况：不拆分最优、拆分入一个月最优、拆分入两个月最优。
2、独立出计算税额的功能函数
3、简化模型，对于拆分入两个月的情况最优解一定是N组解，而不是唯一的，而且这N组解中至少有两月拆入的金额相同的情况。不考虑性能的前提下，我们只关心这组解，以求简化问题。
4、定义个税相关政策的常量，进行初始化

'''
# 主线程执行函数
def run():
    year_bonus = input('Please input bonus\n')
    month_salary = input('Please input salary\n')

    # 获取三种方案的税额（不拆分、拆入一个月、拆入两个月）
    start_time = time.clock()
    year_bonus_tax = get_only_bonus_tax(year_bonus, month_salary)
    one_month_tax = get_one_month_bonus(year_bonus, month_salary)
    two_month_tax = get_two_month_bonus(year_bonus, month_salary)

    # 取最小税额并计算税后奖金
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
    end_time = time.clock()
    print(u"耗时："),
    print (end_time - start_time)
    run()
    return


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
        return 0
    else:
        money -= base_quota
        return money * get_tax_rat(money) - get_tax_quick(money)


# 获取年奖平均月交税金额
def get_per_month_tax(money):
    return money * get_tax_rat(money) - get_tax_quick(money)


# 获取不拆分年奖交税总额
def get_only_bonus_tax(year_bonus, month_salary):
    if month_salary <= base_quota:
        if year_bonus < base_quota - month_salary:
            return 0
        else:
            per_month = (year_bonus - (base_quota - month_salary)) / 12.0
            tax = (year_bonus - (base_quota - month_salary)) * get_tax_rat(per_month) - get_tax_quick(
                per_month)
    else:
        per_month = year_bonus / 12.0
        tax = year_bonus * get_tax_rat(per_month) - get_tax_quick(per_month)

    return tax


# 获取拆分为一个月交税总额
def get_one_month_bonus(year_bonus, month_salary):
    now_bonus_tax = get_only_bonus_tax(year_bonus, month_salary)
    for i in range(1, int(year_bonus)):
        bonus_remain = year_bonus - i
        month_add_salary = month_salary + i
        month_tax_add = get_month_tax(month_add_salary) - get_month_tax(month_salary)
        bonus_tax = round(get_only_bonus_tax(bonus_remain, month_salary) + month_tax_add, 2)

        if bonus_tax < now_bonus_tax:
            now_bonus_tax = bonus_tax
            global one_month
            one_month = i
    return now_bonus_tax


# 获取拆分为两个月交税总额
def get_two_month_bonus(year_bonus, month_salary):
    now_bonus_tax = get_only_bonus_tax(year_bonus, month_salary)
    for i in range(1, int(year_bonus)):
        bonus_remain = year_bonus - i
        month_add_salary = month_salary + (i / 2.0)
        month_tax_add = (get_month_tax(month_add_salary) - get_month_tax(month_salary)) * 2.0
        bonus_tax = round(get_only_bonus_tax(bonus_remain, month_salary) + month_tax_add, 2)

        if bonus_tax < now_bonus_tax:
            now_bonus_tax = bonus_tax
            global two_month
            two_month = i / 2.0
    return now_bonus_tax


# 运行主函数
run()

