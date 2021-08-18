


exp = ExpenditureAmount.query.filter_by(type='Mallory Personal Budget',
                                                year=datetime.now().year,
                                                month=5)

from data import db_query


exp_amt = db_query.extract(exp, 'amount')