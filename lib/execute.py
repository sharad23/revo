## Currently Codes are randomly added. It need to be properly arranged.

import datetime
from collections import OrderedDict


principle_paid_dict = {
    '2/1/2018': 400,
    '3/1/2018': 420
}

interest_paid_dict = {
    '2/1/2018': 20
}


def daily_reporting(**kwargs):
    principle = int(kwargs.get('principle', 1000))
    interest_rate = float(kwargs.get('interest_rate', 0.10))
    grace_period = int(kwargs.get('grace', 3))
    start_date = datetime.datetime.strptime(kwargs.get('start_date', '1/1/2018'), '%d/%m/%Y')
    loan_limit = kwargs.get('loan_limit', 3000)
    due_date = datetime.datetime.strptime(kwargs.get('due_date', '15/1/2018'), '%d/%m/%Y')
    actual_due_date = due_date + datetime.timedelta(days=grace_period)
    principle_paid_dict = kwargs.get('principle_paid_dict', {})
    interest_paid_dict = kwargs.get('interest_paid_dict', {})
    money_borrowed_dict = kwargs.get('money_borrowed_dict', {})
    limit = kwargs.get('days', 27)
    comp_period = int(kwargs.get('comp_period', 360))

    # initialize
    principle_paid = 0
    interest_paid = 0
    outstanding_principle = principle
    outstanding_interest = 0
    principle_overdue = 0
    interest_overdue = 0
    minimum_amount = 0.10*principle
    results = []

    for i in range(1, limit+1):
        date = start_date + datetime.timedelta(days=i-1)


        # find actual_Due_Date
        if grace_period == 0:
            actual_Due_Date = due_date
        else:
            actual_Due_Date = due_date + datetime.timedelta(days=grace_period)


        #interest amount
        interest_amount = 0
        interest_amount = principle * (1 + (interest_rate/comp_period)) - principle if date > actual_Due_Date \
            else interest_amount


        #interest paid
        for key, value in interest_paid_dict.items():
            if date == datetime.datetime.strptime(key, '%d/%m/%Y'):
                interest_paid = value

        #money_borrowed_dict
        money_borrowed = 0
        for key, value in money_borrowed_dict.items():
            if date == datetime.datetime.strptime(key, '%d/%m/%Y'):
                money_borrowed = value

        # 3.principle overdue
        # if actual_Due_Date > date and minimum_amount <= principle_paid:
        #     principle_overdue = 0
        # elif actual_Due_Date < date and minimum_amount >= principle_paid:
        #     principle_overdue = principle - principle_paid
        # elif actual_Due_Date < date and minimum_amount <= principle_paid:
        #     principle_overdue = principle_overdue - principle_paid
        # else:
        #     principle_overdue = 0
        if actual_Due_Date > date and minimum_amount <= principle_paid:
            principle_overdue = 0
        elif actual_Due_Date < date and minimum_amount >= principle_paid:
            principle_overdue = outstanding_principle - principle_paid
        elif actual_Due_Date < date and minimum_amount <= principle_paid:
            principle_overdue = outstanding_principle - principle_paid
        else:
            principle_overdue = 0

        # 1.outstanding principle
        if principle_paid != None:
            principle_paid = 0

        for key, value in principle_paid_dict.items():
            if date == datetime.datetime.strptime(key, '%d/%m/%Y'):
                principle_paid = int(value)
                outstanding_principle = outstanding_principle - principle_paid + money_borrowed
            else:
                outstanding_principle = outstanding_principle + money_borrowed
        #previous line ko outstanding_principle - pri paid + money_borrowed_dict
        #-----------------------------------------------------------


        #2.outstanding interest---------------------------------------
        if actual_Due_Date < date:
            outstanding_interest = outstanding_interest - interest_paid + \
                                   ((outstanding_principle * interest_rate * 1) / comp_period)
        else:
            outstanding_interest = 0
        #-----------------------------------------------------------


        # 4.interest overdue
        interest_overdue = interest_overdue - interest_paid if date > actual_due_date \
            else interest_overdue

        if actual_Due_Date > date:
            interest_overdue = 0
        elif actual_Due_Date < date:
            interest_overdue = outstanding_interest - interest_paid
        else:
            interest_overdue = 0

        result = OrderedDict()
        result['S.No'] = i
        result['Date'] = date.strftime('%d/%m/%Y')
        result['Outstanding Principal'] = round(outstanding_principle, 2)
        result['Outstanding Interest'] = round(outstanding_interest, 2)
        result['Principle Overdue'] = round(principle_overdue, 2)
        result['Interest Overdue'] = round(interest_overdue, 2)
        results.append(result)

    return results


activities = [
    {
        'date': '1/1/2018',
        'interest_paid': 0,
        'money_borrowed': 1000,
        'principle_paid': 2000,

    },
    {
        'date': '3/1/2018',
        'interest_paid': 0,
        'money_borrowed': 1000,
        'principle_paid': 0,
    },
    {
        'date': '5/1/2018',
        'money_borrowed': 0,
        'interest_paid': 100,
        'principle_paid': 1010,
    },
    {
        'date': '5/1/2018',
        'money_borrowed': 0,
        'principle_paid': 0,
        'interest_paid': 1000
    }
]


def transaction_reporting(**kwargs):
    principle = int(kwargs.get('principle', 10000))
    interest_rate = float(kwargs.get('interest_rate', 5/100))
    comp_period = int(kwargs.get('comp_period', 365))
    start_date = datetime.datetime.strptime(kwargs.get('start_date', '1/1/2018'), '%d/%m/%Y')
    activities = kwargs.get('activities', [])
    results = []

    outstanding_principle = principle
    outstanding_interest = 0
    for activity in activities:
        date = datetime.datetime.strptime(activity.get('date'), '%d/%m/%Y')
        interest_paid = activity.get('interest_paid', 0)
        principle_paid = activity.get('principle_paid', 0)
        money_borrowed = activity.get('money_borrowed', 0)

        date_diff = date - start_date
        days = date_diff.days
        outstanding_interest = (outstanding_interest - interest_paid) + \
                               ((outstanding_principle*interest_rate*days) / comp_period)

        outstanding_principle = outstanding_principle - principle_paid + money_borrowed
        results.append({
            'Date': date.strftime('%d/%m/%Y'),
            'Interest Rate': interest_rate,
            'Interest Paid': interest_paid,
            'Principle Paid': principle_paid,
            'Money Brrowed':  money_borrowed,
            'Outstanding Interest': outstanding_interest,
            'Outstanding Principle': outstanding_principle
        })

    return results











def rollover_reporting(**kwargs):
    principle = kwargs.get('principle', 1000)
    interest_rate = kwargs.get('interest_rate', 0.10)
    grace_period = kwargs.get('grace', 3)
    start_date = datetime.datetime.strptime(kwargs.get('start_date', '1/1/2018'), '%d/%m/%Y')
    loan_limit = kwargs.get('loan_limit', 3000)
    due_date = datetime.datetime.strptime(kwargs.get('due_date', '15/1/2018'), '%d/%m/%Y')
    actual_due_date = due_date + datetime.timedelta(days=grace_period)
    principle_paid_dict = kwargs.get('principle_paid_dict', {})
    interest_paid_dict = kwargs.get('interest_paid_dict', {})
    money_borrowed_dict = kwargs.get('money_borrowed_dict', {})
    limit = kwargs.get('limit', 27)
    comp_period = kwargs.get('comp_period', 360)

    r_interest_rate = kwargs.get('r_interest_rate', 0.20)
    r_loan_start_date = datetime.datetime.strptime(kwargs.get('r_loan_start_date', '14/2/2018'), '%d/%m/%Y')
    r_due_date = datetime.datetime.strptime(kwargs.get('r_due_date', '14/2/2018'), '%d/%m/%Y')

    # initialize
    principle_paid = 0
    interest_paid = 0
    outstanding_principle = principle
    outstanding_interest = 0
    principle_overdue = 0
    interest_overdue = 0
    minimum_amount = 0.10*principle
    # print(minimum_amount)
    results = []
    # print(start_date)
    # calculations

    # rollover_dict
    rollover = 0

    for i in range(0, limit+1):
        date = start_date + datetime.timedelta(days=i)
        # print("-------------"+str(i+1)+" "+str(date)+"-------------")

        # find actual_Due_Date
        if grace_period == 0:
            actual_Due_Date = due_date
        else:
            actual_Due_Date = due_date + datetime.timedelta(days=grace_period)


        #interest amount
        interest_amount = 0
        interest_amount = principle * (1 + (interest_rate/comp_period)) - principle  if date > actual_Due_Date \
            else interest_amount


        #interest paid
        for key, value in interest_paid_dict.items():
            if date == datetime.datetime.strptime(key, '%d/%m/%Y'):
                interest_paid = value

        #money_borrowed_dict
        money_borrowed = 0
        for key, value in money_borrowed_dict.items():
            if date == datetime.datetime.strptime(key, '%d/%m/%Y'):
                money_borrowed = value



        # 3.principle overdue
        if actual_Due_Date > date and minimum_amount <= principle_paid:
            principle_overdue = 0
        elif actual_Due_Date < date and minimum_amount >= principle_paid:
            principle_overdue = outstanding_principle - principle_paid
        elif actual_Due_Date < date and minimum_amount <= principle_paid:
            principle_overdue = outstanding_principle - principle_paid
        else:
            principle_overdue = 0


        # 1.outstanding principle
        if principle_paid != None:
            principle_paid = 0

        for key, value in principle_paid_dict.items():
            if actual_Due_Date < date:
                principle_paid = int(value)
                outstanding_principle = outstanding_principle - principle_paid + money_borrowed
            else:
                outstanding_principle = outstanding_principle + money_borrowed
        # principle_paid = 0



        #previous line ko outstanding_principle - pri paid + money_borrowed_dict
        # -----------------------------------------------------------

        #2.outstanding interest---------------------------------------
        if actual_Due_Date < date:
            outstanding_interest = outstanding_interest - interest_paid + \
                                   ((outstanding_principle * interest_rate * 1) / comp_period)
        else:
            outstanding_interest = 0

        #-----------------------------------------------------------






        # 4.interest overdue
        interest_overdue = interest_overdue - interest_paid if date > actual_due_date \
            else interest_overdue

        if actual_Due_Date > date:
            interest_overdue = 0
        elif actual_Due_Date < date:
            interest_overdue = outstanding_interest - interest_paid
        else:
            interest_overdue = 0
        # print(i+1, date.strftime('%d/%m/%Y'),round(outstanding_principle, 2), round(outstanding_interest, 2), round(principle_overdue, 2), round(interest_overdue, 2))





        #rollover_dict
        # r_interest_rate = kwargs.get('r_interest_rate', 0.20)
        # r_loan_start_date = kwargs.get('r_loan_start_date', '14/2/2018')
        # r_due_date = kwargs.get('r_due_date', '18/2/2018')
        # print(outstanding_principle)
        if r_loan_start_date <= date:
            if r_loan_start_date == date:
                roll_outstanding_principle = outstanding_principle


            # print(date)
            # print(r_interest_rate)
            r_principle = outstanding_principle + outstanding_interest
            # print("-------")
            # print(outstanding_principle)
            # print(outstanding_interest)
            # print(r_principle)
            # print("-------")
            interest_rate = r_interest_rate
            actual_Due_Date = r_due_date


            # 3.principle overdue
            if actual_Due_Date > date and minimum_amount <= principle_paid:
                principle_overdue = 0
            elif actual_Due_Date < date and minimum_amount >= principle_paid:
                principle_overdue = outstanding_principle - principle_paid
            elif actual_Due_Date < date and minimum_amount <= principle_paid:
                principle_overdue = outstanding_principle - principle_paid
            else:
                principle_overdue = 0

            # 1.outstanding principle
            if principle_paid != None:
                principle_paid = 0

            # for key, value in principle_paid_dict.items():
            #     if date == datetime.datetime.strptime(key, '%d/%m/%Y'):
            #         principle_paid = int(value)
            #         outstanding_principle = outstanding_principle - principle_paid + money_borrowed
            #     else:
            #         outstanding_principle = outstanding_principle + money_borrowed
            outstanding_principle = r_principle
            if r_loan_start_date == date:
                # print("---^----")
                # print(r_principle)
                outstanding_principle = roll_outstanding_principle
            elif actual_Due_Date >= date:
                outstanding_principle = roll_outstanding_principle


            # principle_paid = 0

            # previous line ko outstanding_principle - pri paid + money_borrowed_dict
            # -----------------------------------------------------------

            # 2.outstanding interest---------------------------------------
            if r_due_date < date:

                outstanding_interest = outstanding_interest - interest_paid + \
                                       ((outstanding_principle * interest_rate * 1) / comp_period)
            else:
                outstanding_interest = 0

            # -----------------------------------------------------------

            # 4.interest overdue
            # interest_overdue = interest_overdue - interest_paid if date > actual_due_date \
            #     else interest_overdue

            if r_due_date > date:
                interest_overdue = 0
            elif r_due_date < date:
                interest_overdue = outstanding_interest - interest_paid
            else:
                interest_overdue = 0
            # print(i+1, date.strftime('%d/%m/%Y'),round(outstanding_principle, 2), round(outstanding_interest, 2), round(principle_overdue, 2), round(interest_overdue, 2))

            result = OrderedDict()
            # results.append(
            #     {
            #         'id': i+1,
            #         'date': date.strftime('%d/%m/%Y'),
            #         # 'interest': round(interest_amount, 3),
            #         'outstanding_principal': round(outstanding_principle, 2),
            #         'outstanding_interest': round(outstanding_interest, 2),
            #         'principle_overdue': round(principle_overdue, 2),
            #         'interest_overdue': round(interest_overdue, 2)
            #     })

            result['S.No'] = i+1
            result['Date'] = date.strftime('%d/%m/%Y')
            result['Outstanding Principal'] = round(outstanding_principle, 2)
            result['Outstanding Interest'] = round(outstanding_interest, 2)
            result['Principle Overdue'] = round(principle_overdue, 2)
            result['Interest Overdue'] = round(interest_overdue, 2)
            results.append(result)

            # return_two_dic = [roll_detail, result]

    return results

def rollover_details(**kwargs):
    principle = kwargs.get('principle', 1000)
    interest_rate = kwargs.get('interest_rate', 0.10)
    grace_period = kwargs.get('grace', 3)
    start_date = datetime.datetime.strptime(kwargs.get('start_date', '1/1/2018'), '%d/%m/%Y')
    loan_limit = kwargs.get('loan_limit', 3000)
    due_date = datetime.datetime.strptime(kwargs.get('due_date', '15/1/2018'), '%d/%m/%Y')
    actual_due_date = due_date + datetime.timedelta(days=grace_period)
    principle_paid_dict = kwargs.get('principle_paid_dict', {})
    interest_paid_dict = kwargs.get('interest_paid_dict', {})
    money_borrowed_dict = kwargs.get('money_borrowed_dict', {})
    limit = kwargs.get('limit', 27)
    comp_period = kwargs.get('comp_period', 360)

    r_interest_rate = kwargs.get('r_interest_rate', 0.20)
    r_loan_start_date = datetime.datetime.strptime(kwargs.get('r_loan_start_date', '14/2/2018'), '%d/%m/%Y')
    r_due_date = datetime.datetime.strptime(kwargs.get('r_due_date', '14/2/2018'), '%d/%m/%Y')

    # initialize
    principle_paid = 0
    interest_paid = 0
    outstanding_principle = principle
    outstanding_interest = 0
    principle_overdue = 0
    interest_overdue = 0
    minimum_amount = 0.10*principle
    # print(minimum_amount)
    results = []
    # print(start_date)
    # calculations

    # rollover_dict
    rollover = 0

    for i in range(0, limit+1):
        date = start_date + datetime.timedelta(days=i)
        # print("-------------"+str(i+1)+" "+str(date)+"-------------")

        # find actual_Due_Date
        if grace_period == 0:
            actual_Due_Date = due_date
        else:
            actual_Due_Date = due_date + datetime.timedelta(days=grace_period)


        #interest amount
        interest_amount = 0
        interest_amount = principle * (1 + (interest_rate/comp_period)) - principle  if date > actual_Due_Date \
            else interest_amount


        #interest paid
        for key, value in interest_paid_dict.items():
            if date == datetime.datetime.strptime(key, '%d/%m/%Y'):
                interest_paid = value

        #money_borrowed_dict
        money_borrowed = 0
        for key, value in money_borrowed_dict.items():
            if date == datetime.datetime.strptime(key, '%d/%m/%Y'):
                money_borrowed = value

        # 3.principle overdue
        if actual_Due_Date > date and minimum_amount <= principle_paid:
            principle_overdue = 0
        elif actual_Due_Date < date and minimum_amount >= principle_paid:
            principle_overdue = outstanding_principle - principle_paid
        elif actual_Due_Date < date and minimum_amount <= principle_paid:
            principle_overdue = outstanding_principle - principle_paid
        else:
            principle_overdue = 0

        # 1.outstanding principle
        if principle_paid != None:
            principle_paid = 0

        for key, value in principle_paid_dict.items():
            if date == datetime.datetime.strptime(key, '%d/%m/%Y'):
                principle_paid = int(value)
                outstanding_principle = outstanding_principle - principle_paid + money_borrowed
            else:
                outstanding_principle = outstanding_principle + money_borrowed

        #2.outstanding interest---------------------------------------
        if actual_Due_Date < date:
            outstanding_interest = outstanding_interest - interest_paid + \
                                   ((outstanding_principle * interest_rate * 1) / comp_period)
        else:
            outstanding_interest = 0

        # 4.interest overdue
        interest_overdue = interest_overdue - interest_paid if date > actual_due_date \
            else interest_overdue

        if actual_Due_Date > date:
            interest_overdue = 0
        elif actual_Due_Date < date:
            interest_overdue = outstanding_interest - interest_paid
        else:
            interest_overdue = 0

        if r_loan_start_date <= date:
            r_principle = outstanding_principle + outstanding_interest
            interest_rate = r_interest_rate
            actual_Due_Date = r_due_date

            # 3.principle overdue
            if actual_Due_Date > date and minimum_amount <= principle_paid:
                principle_overdue = 0
            elif actual_Due_Date < date and minimum_amount >= principle_paid:
                principle_overdue = outstanding_principle - principle_paid
            elif actual_Due_Date < date and minimum_amount <= principle_paid:
                principle_overdue = outstanding_principle - principle_paid
            else:
                principle_overdue = 0

            # 1.outstanding principle
            if principle_paid != None:
                principle_paid = 0
            outstanding_principle = r_principle
            if r_loan_start_date == date:
                # print("---^----")
                # print(r_principle)
                outstanding_principle = r_principle

            # 2.outstanding interest---------------------------------------
            if r_due_date < date:
                outstanding_interest = outstanding_interest - interest_paid + \
                                       ((outstanding_principle * interest_rate * 1) / comp_period)
            else:
                outstanding_interest = 0

            # 4.interest overdue
            if r_due_date > date:
                interest_overdue = 0
            elif r_due_date < date:
                interest_overdue = outstanding_interest - interest_paid
            else:
                interest_overdue = 0
            # print(i+1, date.strftime('%d/%m/%Y'),round(outstanding_principle, 2), round(outstanding_interest, 2), round(principle_overdue, 2), round(interest_overdue, 2))

            result = OrderedDict()
            result['id'] = i+1
            result['date'] = date.strftime('%d/%m/%Y')
            result['outstanding_principal'] = round(outstanding_principle, 2)
            result['outstanding_interest'] = round(outstanding_interest, 2)
            result['principle_overdue'] = round(principle_overdue, 2)
            result['interest_overdue'] = round(interest_overdue, 2)
            results.append(result)

    r_interest_rate = kwargs.get('r_interest_rate', 0.20)
    r_loan_start_date = datetime.datetime.strptime(kwargs.get('r_loan_start_date', '14/2/2018'), '%d/%m/%Y')
    r_due_date = datetime.datetime.strptime(kwargs.get('r_due_date', '14/2/2018'), '%d/%m/%Y')

    roll_details = []
    roll_detail = OrderedDict()

    roll_detail['id'] = "ABC"
    roll_detail['Interest_Rate'] = str(r_interest_rate*100) + "%"
    roll_detail['Loan_Start_Date'] = r_loan_start_date.strftime('%d/%m/%Y')
    roll_detail['Principal_Amount'] = results[0]['outstanding_principal']
    roll_detail['New_Due_Date'] = r_due_date.strftime('%d/%m/%Y')
    roll_details.append(roll_detail)


    return roll_details


def ExistingCreditDetails(**kwargs):
    ReferenceId = kwargs.get('ReferenceId', "ABC")
    InterestRate = kwargs.get('InterestRate', "0.10")
    LoanStartDate = datetime.datetime.strptime(kwargs.get('LoanStartDate', '1/1/2018'), '%d/%m/%Y')
    OutstandingPrincipal = kwargs.get('OutstandingPrincipal', "0.14")
    OutstandingInterest = kwargs.get('OutstandingInterest', "0.14")
    TotalOutstandingAmount = OutstandingPrincipal+OutstandingInterest
    DueDate = datetime.datetime.strptime(kwargs.get('DueDate', '01/02/2018'), '%d/%m/%Y')

    ExistingCreditDetailsResults = []
    ExistingCreditDetailsResult = OrderedDict()

    ExistingCreditDetailsResult['Reference Id'] = ReferenceId
    ExistingCreditDetailsResult['Interest Rate'] = str(InterestRate*100) + "%"
    ExistingCreditDetailsResult['LoanStart Date'] = LoanStartDate.strftime('%d/%m/%Y')
    ExistingCreditDetailsResult['Outstanding Principal'] = OutstandingPrincipal
    ExistingCreditDetailsResult['Outstanding Interest'] = OutstandingInterest
    ExistingCreditDetailsResult['Total Outstanding Amount'] = TotalOutstandingAmount
    ExistingCreditDetailsResult['Due Date'] = DueDate.strftime('%d/%m/%Y')
    ExistingCreditDetailsResults.append(ExistingCreditDetailsResult)

    return ExistingCreditDetailsResults



def emi_cal(**kwargs):

    Amount = kwargs.get('Amount', 10000)
    Yearly_Interest_Rate = kwargs.get('Yearly_Interest_Rate', "0.14")
    Loan_Duration_Months = kwargs.get('Loan_Duration_Months', "Monthly")
    Compounding_Period = kwargs.get('Compounding_Period', "Monthly")
    Start_Date = datetime.datetime.strptime(kwargs.get('Start_Date', '1/11/2017'), '%d/%m/%Y')



    OpeningBalance = 0
    emi_cal_dicts = []
    for each_month in range(1, Loan_Duration_Months+1):

        DueDateofPayment = "1/"+str(each_month)+"/2018"  # Due Date of Payment
        # print(Start_Date)
        # print(Start_Date.month)
        # a = datetime.datetime.strptime('1/'+str(int(Start_Date.month)+int(each_month))+'/2018', '%d/%m/%Y')
        datetime.date(day=1, year=2018, month=1)
        # print(a)


        #Opening Balance
        if OpeningBalance == 0:
            OpeningBalance = Amount
        else:
            OpeningBalance = ClosingBalance

        # print("OpeningBalance: ", OpeningBalance)
        #EMI/ Amount paid
        EMI = (Amount * (Yearly_Interest_Rate/12))/(1-(1+(Yearly_Interest_Rate/12))**-Loan_Duration_Months)

        #Interest
        Interest = OpeningBalance * (Yearly_Interest_Rate/12)
        # print(Interest)

        #Principal
        Principal = EMI - Interest
        # print(Principal)

        #Closing Balance
        ClosingBalance = OpeningBalance - Principal
        # print(ClosingBalance)

        emi_cal_dict = OrderedDict()
        emi_cal_dict['Due Date of Payment'] = DueDateofPayment
        emi_cal_dict['Opening Balance'] = round(OpeningBalance, 2)
        emi_cal_dict['EMI/ Amount paid'] = round(EMI, 2)
        emi_cal_dict['Interest'] = round(Interest, 2)
        emi_cal_dict['Principal'] = round(Principal, 2)
        emi_cal_dict['Closing Balance'] = round(ClosingBalance, 2)
        emi_cal_dicts.append(emi_cal_dict)

    return emi_cal_dicts