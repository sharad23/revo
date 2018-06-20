from lib.execute import daily_reporting, transaction_reporting, rollover_reporting, rollover_details, emi_cal, ExistingCreditDetails
import json
import csv

#1 Transaction
with open('input/Trans.json') as json_data:
    trans = json.load(json_data)
    results = transaction_reporting(**trans)
    # print(results)

    with open('output/Transaction_Report.json', 'w') as fp:
        json.dump(results, fp, indent=4)

    if results:
        keys = results[0].keys()
        with open('output/Transaction_Report.csv', 'w') as csv_file:
            c = csv.writer(csv_file)
            c.writerow(keys)
            for result in results:
                c.writerow(result.values())

#2 Daily
with open('input/Daily_v1.json') as json_data:
    daily = json.load(json_data)
    results = daily_reporting(**daily)

    # result_json = json.dumps(results, indent=3)
    # print(result_json)

    with open('output/Daily_Report.json', 'w') as fp:
        json.dump(results, fp, indent=4)

    if results:
        keys = results[0].keys()
        with open('output/Daily_Report.csv', 'w') as csv_file:
            c = csv.writer(csv_file)
            c.writerow(keys)
            for result in results:
                # split
                # print result.values()[3]
                c.writerow(result.values())

#3 Rollover
with open('input/Rollover.json') as json_data:
    rollover = json.load(json_data)
    results = rollover_reporting(**rollover)
    # print(results)
    with open('output/Rollover_Report.json', 'w') as fp:
        json.dump(results, fp, indent=4)

    if results:
        keys = results[0].keys()
        with open('output/Rollover_Report.csv', 'w') as csv_file:
            c = csv.writer(csv_file)
            c.writerow(keys)
            for result in results:
                # split
                # print result.values()[3]
                c.writerow(result.values())

#4 Rollover Details
with open('input/Rollover.json') as json_data:
    rollover_detail = json.load(json_data)
    results = rollover_details(**rollover_detail)
    # print(results)
    with open('output/Rollover_Details_Report.json', 'w') as fp:
        json.dump(results, fp, indent=4)

    if results:
        keys = results[0].keys()
        with open('output/Rollover_Details_Report.csv', 'w') as csv_file:
            c = csv.writer(csv_file)
            c.writerow(keys)
            for result in results:
                c.writerow(result.values())


#5 Existing Credit Details
with open('input/ExistingCreditDetails.json') as json_data:
    ExistingCreditDetail = json.load(json_data)
    results = ExistingCreditDetails(**ExistingCreditDetail)
    # print(results)
    with open('output/Existing_Credit_Details_Report.json', 'w') as fp:
        json.dump(results, fp, indent=4)

    if results:
        keys = results[0].keys()
        with open('output/Existing_Credit_Details_Report.csv', 'w') as csv_file:
            c = csv.writer(csv_file)
            c.writerow(keys)
            for result in results:
                c.writerow(result.values())


#6 EMI
with open('input/EMI.json') as json_data:
    emi_cal_detail = json.load(json_data)
    results = emi_cal(**emi_cal_detail)
    # print(results)
    with open('output/EMI_Monthly_Report.json', 'w') as fp:
        json.dump(results, fp, indent=4)

    if results:
        keys = results[0].keys()
        with open('output/EMI_Monthly_Report.csv', 'w') as csv_file:
            c = csv.writer(csv_file)
            c.writerow(keys)
            for result in results:
                c.writerow(result.values())
