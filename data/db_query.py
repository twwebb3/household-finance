

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

    df = pd.DataFrame({'type': type,
                       'description': description,
                       'amount': amount})

    return df

