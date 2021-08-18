

def extract(generator, values):
    output = 0
    for i in generator.values(values):
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
    for i in generator.values(value):
        value_dict = i._asdict()
        try:
            output.append(value_dict[value])
        except KeyError:
            print('No values available.')

    return output


def extract_expenditure_history(ExpenditureAmount, type, year, month):
    import pandas as pd

    exp = ExpenditureAmount.query.filter_by(type=type,
                                            year=year).filter(ExpenditureAmount.month >= month)

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
    budget = ExpenditureType.filter_by(expenditure_type=type)
    budget_amt = extract(budget, 'max_amount')
    if type in ('Mallory Personal Budget', 'TW Personal Budget'):
        exp_hist_df = extract_expenditure_history(ExpenditureAmount=ExpenditureAmount,
                                                  type=type,
                                                  year=2020,
                                                  month=9)

    return 0
