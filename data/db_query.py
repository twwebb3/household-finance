

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


def extract_expenditure_history(generator):
    import pandas as pd

    type = extract_list(generator,'type')
    description = extract_list(generator, 'description')
    amount = extract_list(generator, 'amount')

    df = pd.DataFrame({'type': type,
                       'description': description,
                       'amount': amount})

    return df

