

from sqlalchemy.sql import text


def extract(generator, values):
    output = 0
    for i in generator.values(text(values)):
        value_dict = i._asdict()
        try:
            output += value_dict[values]
        except TypeError:
            print('Incorrect value type.')
        except KeyError:
            print('No values available.')

    return output


def extract_list(generator, value):
    output = []
    for i in generator.values(text(value)):
        value_dict = i._asdict()
        try:
            output.append(value_dict[value])
        except KeyError:
            print('No values available.')

    return output


def extract_expenditure_history(ExpenditureAmount, type, year, month):
    import pandas as pd

    exp = ExpenditureAmount.query.filter_by(type=type).filter(ExpenditureAmount.year == year,
                                                              ExpenditureAmount.month == month)
    # duh this wont work have to make a full date column

    type = extract_list(exp,'type')
    description = extract_list(exp, 'description')
    amount = extract_list(exp, 'amount')
    year = extract_list(exp, 'year')
    month = extract_list(exp, 'month')
    day = extract_list(exp, 'day')

    df = pd.DataFrame({'type': type,
                       'description': description,
                       'amount': amount,
                       'year': year,
                       'month': month,
                       'day': day})

    return df


def extract_total_expenditure_history(ExpenditureAmount, type, year):
    import pandas as pd

    exp = ExpenditureAmount.query.filter_by(type=type).filter(ExpenditureAmount.year >= year)
    # duh this wont work have to make a full date column

    type = extract_list(exp,'type')
    description = extract_list(exp, 'description')
    amount = extract_list(exp, 'amount')
    year = extract_list(exp, 'year')
    month = extract_list(exp, 'month')
    day = extract_list(exp, 'day')

    df = pd.DataFrame({'type': type,
                       'description': description,
                       'amount': amount,
                       'year': year,
                       'month': month,
                       'day': day})

    return df


def budget_remaining(ExpenditureType, ExpenditureAmount, type):
    """
    calculates budget remaining for different budget items.
    """
    from datetime import datetime

    start_date = datetime(2020, 9, 1)
    end_date = datetime.now()
    num_months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)

    budget = ExpenditureType.query.filter_by(expenditure_type=type)
    budget_amt = extract(budget, 'max_amount')
    if type in ('Mallory Personal Budget', 'TW Personal Budget'):
        exp_hist_df = extract_total_expenditure_history(ExpenditureAmount=ExpenditureAmount,
                                                        type=type,
                                                        year=2020)

        exp_amount = exp_hist_df.amount.sum()
        budget_amt = budget_amt * num_months
    else:
        exp = ExpenditureAmount.query.filter_by(type=type,
                                                year=datetime.now().year,
                                                month=datetime.now().month)

        exp_amount = extract(exp, 'amount')

    amount = budget_amt - exp_amount

    return amount
