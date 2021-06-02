################# IMPORT PACKAGES  #############################
import pandas as pd
import numpy as np
import numpy_financial as npf
from math import exp, sqrt
import streamlit as st
import matplotlib.pyplot as plt
from itertools import chain
import statistics as stat
from sympy.solvers import solve, solveset, linsolve, nonlinsolve
from sympy import Symbol
import datetime
from random import randint, gauss
from random import randrange
import plotly.express as px
import plotly.figure_factory as ff
from random import gauss
import random

################### CODE ########################################


 
plt.rcParams["font.family"] = "Times New Roman"
st.title("Master Thesis - Fund Simulation Tool")

st.sidebar.title('Parameters')
st.sidebar.markdown('##')
st.sidebar.markdown('##')


# CODE : WATERFALL MODEL
st.subheader('The model assumes the returns of the fund to be distributed by this Waterfall model:')
all_dist = np.zeros((2, 3))
all_dist[:, 0] = [0, 100]
all_dist[:, 1] = [60, 40]
all_dist[:, 2] = [20, 80]
df_dist = pd.DataFrame(all_dist, columns=['IRR < 8%', '8% <= IRR <= 12%', 'IRR > 12%'],
                       index=['% of gain to GP', '% of gain to LP'])

# LAYOUT : WATERFALL MODEL TABLE
st.write((np.transpose(df_dist)))

# CODE: ASSUMPTIONS
st.markdown('#')
st.subheader('Investments are assumed to be done during the first five years of the fund. Choose investment strategy below or'
             ' create your own pace:')

pace = st.selectbox('Select investment pace', ('Choose strategy', 'Generate a Random Pace', 'Deals Linear in Size',
                                               'Big Deals First',
                                               'Create your own investment pace'))
kolumner = []
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
for i in range(10):
    for j in range(12):
        kolumner.append(('Year ' + str(i) + ' - ' + months[j]))

if pace == 'Deals Linear in Size':
    inv_strat = [0.20, 0.20, 0.20, 0.20, 0.20]
    data_2 = np.zeros((1, 5))
    data_2[0, 0] = inv_strat[0]
    data_2[0, 1] = inv_strat[1]
    data_2[0, 2] = inv_strat[2]
    data_2[0, 3] = inv_strat[3]
    data_2[0, 4] = inv_strat[4]
    df_2 = pd.DataFrame(data_2, columns=['Year 1', 'Year 2', 'Year 3', 'Year 4', 'Year 5'])
    fig2, ax2 = plt.subplots()
    ax2.pie(df_2.iloc[0, :], labels=['Year 1', 'Year 2', 'Year 3', 'Year 4', 'Year 5'], autopct='%1.1f%%',
            counterclock=False, colors=['#ff9999', '#c2c2f0', '#99ff99', '#ffcc99', '#ffb3e6'])

    # LAYOUT: PLOT INVESTMENT PACE AS A PIE-CHART
    st.markdown('#')
    st.subheader('The investment pace:')
    st.pyplot(fig2)

elif pace == 'Create your own investment pace':
    year_1 = st.number_input('How much of the committed capital is invested in the first year?(in %)')
    year_2 = st.number_input('How much of the committed capital is invested in the second year?(in %)')
    year_3 = st.number_input('How much of the committed capital is invested in the third year?(in %)')
    year_4 = st.number_input('How much of the committed capital is invested in the fourth year?(in %)')
    year_5 = st.number_input('How much of the committed capital is invested in the fifth year?(in %)')
    if year_1+year_2+year_3+year_4+year_5 != 100 and year_1+year_2+year_3+year_4+year_5 !=0:
        st.write('The pace needs to sum up to 100')

    inv_strat = [year_1/100, year_2/100, year_3/100, year_4/100, year_5/100]
    data_2 = np.zeros((1, 5))
    data_2[0, 0] = inv_strat[0]
    data_2[0, 1] = inv_strat[1]
    data_2[0, 2] = inv_strat[2]
    data_2[0, 3] = inv_strat[3]
    data_2[0, 4] = inv_strat[4]
    df_2 = pd.DataFrame(data_2, columns=['Year 1', 'Year 2', 'Year 3', 'Year 4', 'Year 5'])
    fig2, ax2 = plt.subplots()
    ax2.pie(df_2.iloc[0, :], labels=['Year 1', 'Year 2', 'Year 3', 'Year 4', 'Year 5'], autopct='%1.1f%%',
            counterclock=False, colors=['#ff9999', '#c2c2f0', '#99ff99', '#ffcc99', '#ffb3e6'])

    # LAYOUT: PLOT INVESTMENT PACE AS A PIE-CHART
    st.markdown('#')
    st.subheader('Your created investment pace:')
    st.pyplot(fig2)

elif pace == 'Big Deals First':
    # CODE : INVESTMENTS INFORMATION AND TABLE
    a = random.uniform(0.4, 0.5)
    b = random.uniform(0.2, 1 - a)
    c = random.uniform(0, 1 - (a + b))
    d = random.uniform(0, 1 - (a + b + c))
    e = 1 - a - b - c - d
    numbers = [a, b, c, d, e]
    inv_strat = numbers
    investment_pace = (sorted(numbers, reverse=True))
  #  investment_pace = inv_strat = [0.469, 0.436, 0.056, 0.021, 0.018]

    data_2 = np.zeros((1, 5))
    data_2[0, 0] = investment_pace[0]
    data_2[0, 1] = investment_pace[1]
    data_2[0, 2] = investment_pace[2]
    data_2[0, 3] = investment_pace[3]
    data_2[0, 4] = investment_pace[4]
    df_2 = pd.DataFrame(data_2, columns=['Year 1', 'Year 2', 'Year 3', 'Year 4', 'Year 5'])
    fig2, ax2 = plt.subplots()
    ax2.pie(df_2.iloc[0, :], labels=['Year 1', 'Year 2', 'Year 3', 'Year 4', 'Year 5'], autopct='%1.1f%%',
            counterclock=False, colors=['#ff9999', '#c2c2f0', '#99ff99', '#ffcc99', '#ffb3e6'])

    # LAYOUT: PLOT INVESTMENT PACE AS A PIE-CHART
    st.markdown('#')
    st.subheader('The investment pace')
    st.pyplot(fig2)

elif pace == 'Generate a Random Pace':
    inv_strat = np.zeros(5)
    inv_strat[0:5] = np.random.dirichlet(np.ones(5), size=1)
 #   inv_strat = [0.296, 0.174, 0.283, 0.054, 0.193]
    data_2 = np.zeros((1, 5))
    data_2[0, 0] = inv_strat[0]
    data_2[0, 1] = inv_strat[1]
    data_2[0, 2] = inv_strat[2]
    data_2[0, 3] = inv_strat[3]
    data_2[0, 4] = inv_strat[4]
    df_2 = pd.DataFrame(data_2, columns=['Year 1', 'Year 2', 'Year 3', 'Year 4', 'Year 5'])
    fig2, ax2 = plt.subplots()
    ax2.pie(df_2.iloc[0, :], labels=['Year 1', 'Year 2', 'Year 3', 'Year 4', 'Year 5'], autopct='%1.1f%%',
            counterclock=False, colors=['#ff9999', '#c2c2f0', '#99ff99', '#ffcc99', '#ffb3e6'])
    # LAYOUT: PLOT INVESTMENT PACE AS A PIE-CHART
    st.markdown('#')
    st.subheader('The generated investment pace:')
    st.pyplot(fig2)
else:
    st.text(" ")

st.subheader('Four investments are assumed to be made each year, i.e each third month. Choose a predefined pace below'
             ' or create your own pace')
year_pace = st.selectbox('Select investment pace each year', ('Choose pace', 'Predefined pace',
                                               'Create your own investment pace'))
## INVESTMENT PACE EACH YEAR
if year_pace == 'Predefined pace':
    data = np.zeros((1, 4))
    data[0, 0] = 0.20
    data[0, 1] = 0.35
    data[0, 2] = 0.30
    data[0, 3] = 0.15
    df = pd.DataFrame(data, columns=['January', 'April', 'July', 'October'])
    fig2, ax2 = plt.subplots()
    ax2.pie(df.iloc[0, :], labels=['January', 'April', 'July', 'October'], autopct='%1.1f%%',
            counterclock=False, colors=['#ff9999', '#c2c2f0', '#99ff99', '#ffcc99'])

    # LAYOUT: PLOT INVESTMENT PACE AS A PIE-CHART
    st.markdown('#')
    st.subheader('The investment pace for each year:')
    st.pyplot(fig2)

elif year_pace == 'Create your own investment pace':

    year_jan = st.number_input('How much of the yearly investment is invested in January? (in %)')
    year_april = st.number_input('How much of the yearly investment is invested in April? (in %)')
    year_july = st.number_input('How much of the yearly investment is invested in July? (in %)')
    year_oct = st.number_input('HHow much of the yearly investment is invested in October? (in %)')
    if year_jan + year_april + year_july + year_oct  != 100 and year_jan + year_april + year_july + year_oct  != 0:
        st.write('The pace need to sum up to 100')

    inv_strat_ = [year_jan / 100, year_april / 100, year_july / 100, year_oct / 100]
    data = np.zeros((1, 4))
    data[0, 0] = inv_strat_[0]
    data[0, 1] = inv_strat_[1]
    data[0, 2] = inv_strat_[2]
    data[0, 3] = inv_strat_[3]

    df = pd.DataFrame(data, columns=['January', 'April', 'July', 'October'])
    fig2, ax2 = plt.subplots()
    ax2.pie(df.iloc[0, :], labels=['January', 'April', 'July', 'October'], autopct='%1.1f%%',
            counterclock=False, colors=['#ff9999', '#c2c2f0', '#99ff99', '#ffcc99'])

    st.markdown('#')
    st.subheader('Your created investment pace for each year:')
    st.pyplot(fig2)


if year_pace != 'Choose pace':
    st.markdown('#')
    st.header('Comparison between different bridge facility and installment strategies')
    st.subheader('Four different strategies are defined, see below:')
    st.text('- No usage of SLCs')
    st.text('- Installment Strategy 1: Repay each bridge facility after 12 months')
    st.text('- Installment Strategy 2: Repay each bridge facility before taking a new loan')
    st.text('- Installment Strategy 3: Repay all bridge facilities once a year, i.e all together')
    st.markdown('#')

    st.subheader('Which strategies do you want to compare?')
    comp_strat = st.selectbox('Choose which strategies to compare', ('Choose strategies',
                                                                     'No SLCs and Installment Strategy 1',
                                                                     'No SLCs and Installment Strategy 2',
                                                                     'No SLCs and Installment Strategy 3',
                                                                     'Installment Strategy 1 and Installment Strategy 2',
                                                                     'Installment Strategy 1 and Installment Strategy 3',
                                                                     'Installment Strategy 2 and Installment Strategy 3',
                                                                     'No SLCs, Installment Strategy 1 and Installment Strategy 2',
                                                                     'No SLCs, Installment Strategy 1 and Installment Strategy 3',
                                                                     'No SLCs, Installment Strategy 2 and Installment Strategy 3',
                                                                     'Installment Strategy 1, Installment Strategy 2 and'
                                                                     ' Installment Strategy 3',
                                                                     'All four strategies'))



    if comp_strat != 'Choose strategies':

        # Volatility and Expected Value and Cholesky Correlation

        st.markdown('##')
        st.subheader('What type of fund do you want to simulate?')
        st.write('The Target-IRR, the correlation between the investments and the volatilty of the investments will be '
                 'determined based on your choice of fund. You can also choose to set your own value to these parameters:')
        ## select fund type
        business_line = st.selectbox(
            'Select Business Segment: Private Capital, Real Assets or Choose the Target IRR, Volatility and Correlation below'
            , ('Equity', 'Mid Market', 'Infrastructure', 'Choose Parameters'))

        if business_line == 'Equity':
            mu1 = 22.5
            sigma1 = 0.2520589140287484 * 100
            corr1 = 0.21826784981672262 * 100

        elif business_line == 'Mid Market':
            mu1 = 22.5
            sigma1 = 0.248*100
            corr1 = 0.197*100

        elif business_line == 'Infrastructure':
            mu1 = 15
            sigma1 = 0.303*100
            corr1 = 0.192 *100

        elif business_line == 'Choose Parameters':
            mu1 = st.number_input('Set the drift (Target IRR) in %',
                                  min_value=0.0, max_value=100.0, value=12.0)  # 0.02
            sigma1 = st.number_input('Set the volatility (standard deviation), in %',
                                     min_value=0.0, max_value=100.0, value=10.0)  # 0.6
            corr1 = st.number_input('Set the correlation between the investments, in %',
                                    min_value=0.0, max_value=100.0, value=20.0)  # 0.6

        st.write('Market estimation of:')
        #st.write('Target IRR', mu1,'%')
        st.write('Volatility', sigma1,'%')
        st.write('Correlation', corr1, '%')



        #######################################

    # START

    ######################################
    #                                    #
    #               CASE 1               #
    #                                    #
    ######################################
        st.markdown('#')
        st.sidebar.subheader("Amount of committed capital")
        com_cap = st.sidebar.number_input('How much is the committed capital?', value=1000000000)
        buffer = st.sidebar.number_input('How much will be kept as a buffer, in %?', min_value=0.0, max_value=100.0,
                                         value=20.0)
        invest_amount = (100 - buffer) / 100
        com_cap = com_cap - com_cap * (buffer / 100)
        st.sidebar.markdown('##')


        int_loan = st.sidebar.number_input('What is the Bridge Facility Interest Rate? (per year in %)', value=1.0)
        st.sidebar.markdown('#')

        e_i = st.sidebar.number_input('What is the Eligible Investor Ratio? (i.e the credit worthiness of the investors, 0 - 1.0)',
                                      value = 0.9)
        st.sidebar.markdown('#')

        st.sidebar.subheader('Number of simulations')
        sim = st.sidebar.slider('How many simulations do you want to generate?', 0, 100000, 10, 1)

        monthly_int = ((int_loan * 0.01) / 12)
        mgm_fee_perc = 0.01
        mgm_fee_yearly = mgm_fee_perc * com_cap

        years = 5

        perc = [0.20, 0.35, 0.30, 0.15]
        inv = np.zeros(12 * years)
        length = len(inv)

        mgm_fee_vector = np.zeros(length)

        counter = 0
        for i in np.arange(0, 12 * years, 12):
            inv[i] = com_cap * perc[0] * inv_strat[counter]
            inv[i + 3] = com_cap * perc[1] * inv_strat[counter]
            inv[i + 6] = com_cap * perc[2] * inv_strat[counter]
            inv[i + 9] = com_cap * perc[3] * inv_strat[counter]
            if i > 0:
                mgm_fee_vector[i] = mgm_fee_yearly
            counter = counter + 1

        if comp_strat == 'No SLCs and Installment Strategy 1':
            fin_stra = ['Do not use SLCs','Repay each loan after 12 months']
        elif comp_strat == 'No SLCs and Installment Strategy 2':
            fin_stra = ['Do not use SLCs', 'Repay each loan before taking a new one']
        elif comp_strat == 'No SLCs and Installment Strategy 3':
            fin_stra = ['Do not use SLCs', 'Repay loans once a year, i.e all together']
        elif comp_strat == 'Installment Strategy 1 and Installment Strategy 2':
            fin_stra = ['Repay each loan after 12 months','Repay each loan before taking a new one']
        elif comp_strat == 'Installment Strategy 1 and Installment Strategy 3':
            fin_stra = ['Repay each loan after 12 months','Repay loans once a year, i.e all together']
        elif comp_strat == 'Installment Strategy 2 and Installment Strategy 3':
            fin_stra = ['Repay each loan before taking a new one','Repay loans once a year, i.e all together']
        elif comp_strat == 'No SLCs, Installment Strategy 1 and Installment Strategy 2':
            fin_stra = ['Do not use SLCs','Repay each loan after 12 months','Repay each loan before taking a new one']
        elif comp_strat == 'No SLCs, Installment Strategy 1 and Installment Strategy 3':
            fin_stra = ['Do not use SLCs','Repay each loan after 12 months','Repay loans once a year, i.e all together']
        elif comp_strat == 'No SLCs, Installment Strategy 2 and Installment Strategy 3':
            fin_stra = ['Do not use SLCs','Repay each loan before taking a new one','Repay loans once a year, i.e all together']
        elif comp_strat == 'Installment Strategy 1, Installment Strategy 2 and Installment Strategy 3':
            fin_stra = ['Do not use SLCs','Repay each loan before taking a new one','Repay loans once a year, i.e all together']
        else:
            fin_stra = ['Do not use SLCs', 'Repay each loan after 12 months','Repay each loan before taking a new one',
                        'Repay loans once a year, i.e all together']


        if comp_strat != 'Choose strategies':
            net_IRR_test = np.zeros(sim * len(fin_stra))
            gross_IRR_test = np.zeros(sim * len(fin_stra))

            lp_test = np.zeros(sim * len(fin_stra))
            gp_test = np.zeros(sim * len(fin_stra))
            lp_tier_1 = np.zeros(sim * len(fin_stra))
            gp_tier_1 = np.zeros(sim * len(fin_stra))
            lp_tier_2 = np.zeros(sim * len(fin_stra))
            gp_tier_2 = np.zeros(sim * len(fin_stra))

            lp_gross_bracket = np.zeros(18*len(fin_stra)) #sim * len(fin_stra))
            gp_gross_bracket = np.zeros(18*len(fin_stra)) #sim * len(fin_stra))
            gp_gross_bracket_1 = np.zeros(18 * len(fin_stra))
            gp_gross_bracket_2 = np.zeros(18 * len(fin_stra))  # sim * len(fin_stra))


            for k in range(len(fin_stra)):
                fin_strat = fin_stra[k]

                drawn_cap = np.zeros(length)
                loan_allowance = np.zeros(length)
                loan_out = np.zeros(length)
                loan_left = np.zeros(length)
                loan_taken = np.zeros(length)
                loan_cost = np.zeros(length)
                loan_repay = np.zeros(length)
                drawn_cumsum = np.zeros(length)
                paid_int = np.zeros(length)


                if fin_strat == 'Repay each loan after 12 months':

                    st.markdown('##')
                    st.header('Installment Strategy 1:')
                    st.subheader('Repay each loan after 12 months')
                    st.markdown('#')

                    for i in range(length):
                        loan_allowance[i] = max((min((com_cap - drawn_cumsum[i]) * e_i, 0.35 * com_cap)), 0)

                        if i == 0:
                            loan_left[i] = loan_allowance[i]

                            if loan_left[i] > inv[i]:
                                loan_taken[i] = inv[i]
                            else:
                                loan_taken[i] = loan_left[i]
                                drawn_cap[i] = inv[i] - loan_taken[i]
                            loan_out[i] = loan_out[i] + loan_taken[i]
                            loan_left[i] = loan_left[i] - loan_taken[i] #

                        if (i > 0 and i < 59):
                            drawn_cumsum[i] = np.sum(drawn_cap)
                            loan_allowance[i] = max((min((com_cap - drawn_cumsum[i]) * e_i, 0.35 * com_cap)), 0)

                            if loan_taken[i - 12] != 0:
                                loan_repay[i] = loan_taken[i - 12]
                                paid_int[i] = np.sum(loan_cost) - np.sum(paid_int[0:i])
                                drawn_cap[i] = loan_repay[i] + paid_int[i]
                            else:
                                loan_repay[i] = 0

                            loan_left[i] = loan_left[i - 1] + loan_repay[i]
                            loan_out[i] = loan_out[i - 1] - loan_repay[i]

                            if inv[i] > 0 and inv[i] > loan_left[i]:
                                loan_taken[i] = loan_left[i]
                                loan_left[i] = 0
                                loan_out[i] = loan_allowance[i]
                                drawn_cap[i] = drawn_cap[i] + inv[i] - loan_taken[i]

                            elif inv[i] > 0 and inv[i] < loan_left[i]:
                                loan_taken[i] = inv[i]
                                loan_out[i] = loan_out[i] + loan_taken[i]

                            if loan_out[i] > loan_allowance[i]:
                                loan_out[i] = loan_allowance[i]
                                loan_repay[i] = loan_repay[i] + (loan_out[i]-loan_allowance[i])
                                drawn_cap[i] = drawn_cap[i] + loan_repay[i]

                        drawn_cap[i] = drawn_cap[i] + mgm_fee_vector[i]
                        loan_cost[i] = monthly_int * loan_out[i]
                        loan_left[i] = loan_allowance[i] - loan_out[i]

                        if i == 59:
                            loan_repay[i] = loan_out[i - 1]
                            loan_left[i] = loan_allowance[i]
                            loan_out[i] = 0
                            paid_int[i] = np.sum(loan_cost) - np.sum(paid_int)
                            drawn_cap[i] = drawn_cap[i] + loan_repay[i] + paid_int[i]

                    cumsum_mgm_fees = np.cumsum(mgm_fee_vector)
                    cumsum_drawn_cap = np.cumsum(drawn_cap)
                    cumsum_loan_cost = np.cumsum(loan_cost)
                    cumsum_paid_int = np.cumsum(paid_int)
                    cumsum_inv_cap = np.cumsum(inv)

                    df = pd.DataFrame(
                        [inv, cumsum_inv_cap, loan_allowance, loan_taken, loan_out, loan_left, loan_repay, loan_cost,
                         cumsum_loan_cost, paid_int, cumsum_paid_int, mgm_fee_vector,
                         cumsum_mgm_fees, drawn_cap, cumsum_drawn_cap],
                        index=['Investment', 'Total Invested Capital',
                               'Loan Allowance', 'Loan Taken', 'Loan Outstanding', 'Loan not used',
                               'Loan repayment',
                               'Loan interests cost', 'Total Loan Costs', 'Paid Loan Costs', 'Total Paid Interest',
                               'Management fees', 'Total Management fees', 'Drawn Capital',
                               'Total Drawn Capital'],
                        columns=kolumner[0:60])

                    st.write('Investment table')

                    if st.checkbox('Show investment table',key='inv_1'):
                        st.write(df)

                    realization = com_cap - cumsum_inv_cap

                    mgm_fee_div = np.zeros(length)
                    for i in range(length):
                        mgm_fee_div[i] = mgm_fee_perc * realization[i - 60]

                    div_cap = np.zeros(length)
                    div_yearly = np.zeros(length)
                    div_total = com_cap * np.ones(length)
                    cumsum_mgm_fees_div = np.cumsum(mgm_fee_div)
                    drawn_cap_div = mgm_fee_div
                    cumsum_drawn_cap_div = np.cumsum(mgm_fee_div) + com_cap

                    df_div = pd.DataFrame([div_cap, div_yearly, div_total, realization, mgm_fee_div, cumsum_mgm_fees_div,
                                           drawn_cap_div, cumsum_drawn_cap_div],
                                          index=['Divested Capital', 'Divested Capital Yearly', 'Total Divested Capital',
                                                 'Realization', 'Management fees', 'Total Management fees', 'Drawn Capital',
                                                 'Total Drawn Capital']
                                          , columns=kolumner[60:120])

                    st.markdown('#')
                    st.write('Divestment table')
                    if st.checkbox('Show divestment table',key='div_1'):
                        st.write(df_div)
                    # divestment table


                ######################################
                #                                    #
                #               CASE 3               #
                #                                    #
                ######################################
                elif fin_strat == 'Repay each loan before taking a new one':

                    st.markdown('##')
                    st.header('Installment Strategy 2:')
                    st.subheader('Repay each loan after 3 months, i.e before new loan')
                    st.markdown('#')

                    for i in range(length):
                        # loan_allowance[i] = min((com_cap - drawn_cap[i]) * e_i, 0.35 * com_cap)
                        #loan_allowance[i] = min((com_cap - drawn_cumsum[i]) * e_i, 0.35 * com_cap)
                        loan_allowance[i] = max((min((com_cap - drawn_cumsum[i]) * e_i, 0.35 * com_cap)), 0)

                        if i == 0:
                            loan_left[i] = loan_allowance[i]

                            if loan_left[i] > inv[i]:
                                loan_taken[i] = inv[i]
                            else:
                                loan_taken[i] = loan_left[i]
                                drawn_cap[i] = inv[i] - loan_taken[i]
                            loan_out[i] = loan_out[i] + loan_taken[i]
                        loan_left[i] = loan_left[i] - loan_taken[i]

                        if i > 0:
                            drawn_cumsum[i] = np.sum(drawn_cap)
                            loan_allowance[i] = max((min((com_cap - drawn_cumsum[i]) * e_i, 0.35 * com_cap)), 0)

                            if loan_taken[i - 3] != 0:
                                loan_repay[i] = loan_taken[i - 3]
                                paid_int[i] = np.sum(loan_cost) - np.sum(paid_int[0:i])
                                drawn_cap[i] = loan_repay[i] + paid_int[i]
                            else:
                                loan_repay[i] = 0
                            loan_left[i] = loan_left[i - 1] + loan_repay[i]
                            loan_out[i] = loan_out[i - 1] - loan_repay[i]

                            if inv[i] > 0 and inv[i] > loan_left[i]:
                                loan_taken[i] = loan_left[i]
                                loan_left[i] = 0
                                loan_out[i] = loan_allowance[i]
                                drawn_cap[i] = drawn_cap[i] + inv[i] - loan_taken[i]

                            elif inv[i] > 0 and inv[i] < loan_left[i]:
                                loan_taken[i] = inv[i]
                                loan_out[i] = loan_out[i] + loan_taken[i]
                                loan_left[i] = loan_left[i] - loan_taken[i]

                        if loan_out[i] > loan_allowance[i]:
                            loan_out[i] = loan_allowance[i]
                            loan_repay[i] = loan_repay[i] + (loan_out[i]-loan_allowance[i])
                            drawn_cap[i] = drawn_cap[i] + loan_repay[i]

                        drawn_cap[i] = drawn_cap[i] + mgm_fee_vector[i]
                        loan_cost[i] = monthly_int * loan_out[i]
                        loan_left[i] = loan_allowance[i] - loan_out[i]

                        if i == 59:
                            loan_repay[i] = loan_out[i - 1]
                            loan_left[i] = loan_allowance[i]
                            loan_out[i] = 0
                            paid_int[i] = np.sum(loan_cost) - np.sum(paid_int)
                            drawn_cap[i] = drawn_cap[i] + loan_repay[i] + paid_int[i]

                    cumsum_mgm_fees = np.cumsum(mgm_fee_vector)
                    cumsum_drawn_cap = np.cumsum(drawn_cap)
                    cumsum_loan_cost = np.cumsum(loan_cost)
                    cumsum_paid_int = np.cumsum(paid_int)
                    cumsum_inv_cap = np.cumsum(inv)
                    df = pd.DataFrame([inv, loan_allowance, loan_taken, loan_out, loan_left, loan_repay, loan_cost,
                                       cumsum_loan_cost, paid_int, cumsum_paid_int, mgm_fee_vector,
                                       cumsum_mgm_fees, drawn_cap, cumsum_drawn_cap],
                                      index=['Investment', 'Loan Allowance', 'Loan Taken', 'Loan Outstanding', 'Loan not used',
                                             'Loan repayment',
                                             'Loan interests cost', 'Total Loan Costs', 'Paid Loan Costs',
                                             'Total Paid Interest',
                                             'Management fees', 'Total Management fees', 'Drawn Capital',
                                             'Total Drawn Capital'],
                                      columns=kolumner[0:60])
                    st.write('Investment table')
                    if st.checkbox('Show investment table',key='inv_2'):
                        st.write(df)

                    st.markdown('##')

                    realization = com_cap - cumsum_inv_cap

                    mgm_fee_div = np.zeros(length)
                    for i in range(length):
                        mgm_fee_div[i] = mgm_fee_perc * realization[i - 60]

                    div_cap = np.zeros(length)
                    div_yearly = np.zeros(length)
                    div_total = com_cap * np.ones(length)
                    cumsum_mgm_fees_div = np.cumsum(mgm_fee_div)
                    drawn_cap_div = mgm_fee_div
                    cumsum_drawn_cap_div = np.cumsum(mgm_fee_div) + com_cap

                    df_div = pd.DataFrame([div_cap, div_yearly, div_total, realization, mgm_fee_div, cumsum_mgm_fees_div,
                                           drawn_cap_div, cumsum_drawn_cap_div],
                                          index=['Divested Capital', 'Divested Capital Yearly', 'Total Divested Capital',
                                                 'Realization', 'Management fees', 'Total Management fees', 'Drawn Capital',
                                                 'Total Drawn Capital']
                                          , columns=kolumner[60:120])
                    st.write('Divestment table')
                    if st.checkbox('Show divestment table',key='div_2'):
                        st.write(df_div)

                ######################################
                #                                    #
                #               CASE 4               #
                #                                    #
                ######################################

                elif fin_strat == 'Repay loans once a year, i.e all together':
                    st.markdown('##')
                    st.header('Installment Strategy 3:')
                    st.subheader('Repay the loans once a year, i.e after 12 months')
                    st.markdown('#')
                    counter = 0

                    for i in np.arange(0, 12 * years, 12):
                        inv[i] = com_cap * perc[0] * inv_strat[counter]
                        inv[i + 3] = com_cap * perc[1] * inv_strat[counter]
                        inv[i + 6] = com_cap * perc[2] * inv_strat[counter]
                        inv[i + 9] = com_cap * perc[3] * inv_strat[counter]
                        if i > 0:
                            mgm_fee_vector[i] = mgm_fee_yearly
                        counter = counter + 1

                    for i in range(length):
                        loan_allowance[i] = max((min((com_cap - drawn_cumsum[i]) * e_i, 0.35 * com_cap)), 0)

                        if i == 0:
                            loan_left[i] = loan_allowance[i]

                            if loan_left[i] > inv[i]:
                                loan_taken[i] = inv[i]
                            else:
                                loan_taken[i] = loan_left[i]
                                drawn_cap[i] = inv[i] - loan_taken[i]
                            loan_out[i] = loan_out[i] + loan_taken[i]
                        loan_left[i] = loan_left[i] - loan_taken[i]

                        if i > 0:
                            drawn_cumsum[i] = np.sum(drawn_cap)
                            loan_allowance[i] = max((min((com_cap - drawn_cumsum[i]) * e_i, 0.35 * com_cap)), 0)

                            if i in [12, 24, 36, 48, 60]:
                                loan_repay[i] = loan_out[i - 1]  # loan_taken[i-3]
                                paid_int[i] = np.sum(loan_cost) - np.sum(paid_int[0:i])
                                drawn_cap[i] = loan_repay[i] + paid_int[i]
                            else:
                                loan_repay[i] = 0
                            loan_left[i] = loan_left[i - 1] + loan_repay[i]
                            loan_out[i] = loan_out[i - 1] - loan_repay[i]

                            if inv[i] > 0 and inv[i] > loan_left[i]:
                                loan_taken[i] = loan_left[i]
                                loan_left[i] = 0
                                loan_out[i] = loan_allowance[i]
                                drawn_cap[i] = drawn_cap[i] + inv[i] - loan_taken[i]

                            elif inv[i] > 0 and inv[i] < loan_left[i]:
                                loan_taken[i] = inv[i]
                                loan_out[i] = loan_out[i] + loan_taken[i]
                                loan_left[i] = loan_left[i] - loan_taken[i]

                        if loan_out[i] > loan_allowance[i]:
                            loan_out[i] = loan_allowance[i]
                            loan_repay[i] = loan_repay[i] + (loan_out[i]-loan_allowance[i])
                            drawn_cap[i] = drawn_cap[i] + loan_repay[i]

                        drawn_cap[i] = drawn_cap[i] + mgm_fee_vector[i]
                        loan_cost[i] = monthly_int * loan_out[i]
                        loan_left[i] = loan_allowance[i] - loan_out[i]

                        if i == 59:
                            loan_repay[i] = loan_out[i - 1]
                            loan_left[i] = loan_allowance[i]
                            loan_out[i] = 0
                            paid_int[i] = np.sum(loan_cost) - np.sum(paid_int)
                            drawn_cap[i] = drawn_cap[i] + loan_repay[i] + paid_int[i]

                    cumsum_mgm_fees = np.cumsum(mgm_fee_vector)
                    cumsum_drawn_cap = np.cumsum(drawn_cap)
                    cumsum_loan_cost = np.cumsum(loan_cost)
                    cumsum_paid_int = np.cumsum(paid_int)
                    df = pd.DataFrame([inv, loan_allowance, loan_taken, loan_out, loan_left, loan_repay, loan_cost,
                                       cumsum_loan_cost, paid_int, cumsum_paid_int, mgm_fee_vector,
                                       cumsum_mgm_fees, drawn_cap, cumsum_drawn_cap],
                                      index=['Investment', 'Loan Allowance', 'Loan Taken', 'Loan Outstanding', 'Loan not used',
                                             'Loan repayment',
                                             'Loan interests cost', 'Total Loan Costs', 'Paid Loan Costs',
                                             'Total Paid Interest',
                                             'Management fees', 'Total Management fees', 'Drawn Capital',
                                             'Total Drawn Capital'],
                                      columns=kolumner[0:60])

                    st.write('Investment table')
                    if st.checkbox('Show investment table',key='inv_3'):
                        st.write(df)
                    st.markdown('##')

                    cumsum_inv_cap = np.cumsum(inv)
                    realization = com_cap - cumsum_inv_cap

                    mgm_fee_div = np.zeros(length)
                    for i in range(length):
                        mgm_fee_div[i] = mgm_fee_perc * realization[i - 60]

                    div_cap = np.zeros(length)
                    div_yearly = np.zeros(length)
                    div_total = com_cap * np.ones(length)
                    cumsum_mgm_fees_div = np.cumsum(mgm_fee_div)
                    drawn_cap_div = mgm_fee_div
                    cumsum_drawn_cap_div = np.cumsum(mgm_fee_div) + com_cap

                    df_div = pd.DataFrame([div_cap, div_yearly, div_total, realization, mgm_fee_div, cumsum_mgm_fees_div,
                                           drawn_cap_div, cumsum_drawn_cap_div],
                                          index=['Divested Capital', 'Divested Capital Yearly', 'Total Divested Capital',
                                                 'Realization', 'Management fees', 'Total Management fees', 'Drawn Capital',
                                                 'Total Drawn Capital']
                                          , columns=kolumner[60:120])
                    st.write('Divestment table')
                    if st.checkbox('Show divestment table',key='div_3'):
                        st.write(df_div)


                ######################################
                #                                    #
                #         CASE 5- NO LOAN            #
                #                                    #
                ######################################
                elif fin_strat == 'Do not use SLCs':
                    st.markdown('#')
                    st.header('RESULTS SECTION')

                    st.markdown('##')
                    st.header('No loan scenario')

                    for i in range(length):
                        drawn_cap[i] = inv[i] + mgm_fee_vector[i]

                    cumsum_mgm_fees = np.cumsum(mgm_fee_vector)
                    cumsum_drawn_cap = np.cumsum(drawn_cap)

                    df = pd.DataFrame([inv, mgm_fee_vector,
                                       cumsum_mgm_fees, drawn_cap, cumsum_drawn_cap],
                                      index=['Investment',
                                             'Management fees', 'Total Management fees', 'Drawn Capital',
                                             'Total Drawn Capital'],
                                      columns=kolumner[0:60])

                    st.write('Investment table')
                    if st.checkbox('Show investment table',key='inv_no'):
                        st.write(df)
                    st.markdown('##')

                    cumsum_inv_cap = np.cumsum(inv)
                    realization = com_cap - cumsum_inv_cap

                    mgm_fee_div = np.zeros(length)
                    for i in range(length):
                        mgm_fee_div[i] = mgm_fee_perc * realization[i - 60]

                    div_cap = np.zeros(length)
                    div_yearly = np.zeros(length)
                    div_total = com_cap * np.ones(length)
                    cumsum_mgm_fees_div = np.cumsum(mgm_fee_div)
                    drawn_cap_div = mgm_fee_div
                    cumsum_drawn_cap_div = np.cumsum(mgm_fee_div) + com_cap

                    df_div = pd.DataFrame([div_cap, div_yearly, div_total, realization, mgm_fee_div, cumsum_mgm_fees_div,
                                           drawn_cap_div, cumsum_drawn_cap_div],
                                          index=['Divested Capital', 'Divested Capital Yearly', 'Total Divested Capital',
                                                 'Realization', 'Management fees', 'Total Management fees', 'Drawn Capital',
                                                 'Total Drawn Capital']
                                          , columns=kolumner[60:120])
                    st.write('Divestment table')
                    if st.checkbox('Show divestment table',key='div_no'):
                        st.write(df_div)

                else:
                    st.text(" ")


            ###

                if pace != 'Choose strategy' and fin_strat != 'Choose strategy':
                    rader = []
                    for i in range(20):
                        rader.append('Investment ' + str(i + 1))

                    # Create investment matrix, size 20*120
                    sim_inv = np.zeros((20, 120))

                    for i in range(20):
                        if i < 4:
                            sim_inv[i, i * 3] = inv_strat[0] * perc[i] * com_cap
                        elif i >= 4 and i < 8:
                            sim_inv[i, i * 3] = inv_strat[1] * perc[i - 4] * com_cap
                        elif i >= 8 and i < 12:
                            sim_inv[i, i * 3] = inv_strat[2] * perc[i - 8] * com_cap
                        elif i >= 12 and i < 16:
                            sim_inv[i, i * 3] = inv_strat[2] * perc[i - 12] * com_cap
                        else:
                            sim_inv[i, i * 3] = inv_strat[3] * perc[i - 16] * com_cap

                    df_inv = pd.DataFrame(sim_inv, columns=kolumner, index=rader)

                    st.markdown('#')
                    st.write('Initial investments')

                    if st.checkbox('Show initial investment table',key='ini_inv'+str(k)):
                        st.write(df_inv)
                    st.markdown('#')

                    mu = (mu1 / (12)) / 100
                    sigma = (sigma1 / np.sqrt(12)) / 100
                    corr_inv = corr1 / 100


                    correlation_investments = np.ones((20, 20)) * corr_inv
                    row, col = np.diag_indices(correlation_investments.shape[0])
                    correlation_investments[row, col] = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
                    chol_matrix = np.linalg.cholesky(correlation_investments)


                    # LAYOUT : SIMULATION WITH GBM, SET NUMBER IN SIDEBAR
                    st.subheader('Simulations with Geometric Brownian Motion')
                  #  if st.button('Start the simulation of the funds', key='sim'+str(k)):


                    st.write("Now we are simulating the investment value over the years by using the GBM formula,"
                             " the number of simulations are set to", sim)

                    IRR = np.zeros(sim)
                    RM = np.zeros(sim)
                    gross_IRR = np.zeros(sim)
                    MOIC = np.zeros(sim)




                    LP = np.zeros(sim)
                    GP = np.zeros(sim)

                    tier_1_LP = np.zeros(sim);
                    tier_1_GP = np.zeros(sim)
                    tier_2_LP = np.zeros(sim);
                    tier_2_GP = np.zeros(sim)

                    exit_each_month = np.zeros((sim, 60))
                    exit_each_month_120 = np.zeros((sim, 120))

                    irr_12_amount = 0


                    drawn_cap_total = np.zeros(120)
                    drawn_cap_total[0:60] = drawn_cap
                    drawn_cap_total[60:120] = drawn_cap_div


                    for i in range(len(drawn_cap_total)):
                        irr_12_amount = irr_12_amount + (drawn_cap_total[i]) / (
                                (1 + 0.12) ** (len(drawn_cap_total) - i))

                    for s in range(sim):

                    # Counter simulations:
                      #  if s in [10000,20000,30000,40000,50000,60000,70000,80000,90000]:
                       #     st.write(s)

                        simulated_investments = np.zeros((20, 120))
                        simulated_investments[0:20, 0:120] = sim_inv

                        for j in range(120 - 1):
                            random_numbers = np.random.normal(0, 1, 20)
                            error = np.zeros(20)

                            for i in np.arange(0, 20):
                                error[i] = np.dot(chol_matrix[i, :], random_numbers)

                                # Random holding period line:
                                # investment_length = random.randint(2,6)

                                # Fixed holding period, 60 months, i.e 5 years
                                investment_length = 60

                                if simulated_investments[i, j] != 0 and (
                                        simulated_investments[i, :] == 0).sum() != investment_length:
                                    simulated_investments[i, j + 1] = simulated_investments[i, j] * np.exp(
                                        (mu - (sigma ** 2) / 2) + (sigma * error[i]))

                        for i in range(20):
                            exit_each_month_120[s, 59 + i * 3] = simulated_investments[i, 59 + i * 3]

                        cf_in = drawn_cap_total
                        cf_out = exit_each_month_120[s, :]  # np.array(exit_each_year_s[s,:])
                        cf_total = np.zeros(120)
                        cf_total[0:120] = - cf_in + cf_out
                        IRR[s] = npf.irr(cf_total) * 12  # times 12 in order to get yearly IRR not monthly
                        total_exit = np.sum(exit_each_month_120[s, :])
                        MOIC[s] = total_exit / com_cap

                        if k > 0:
                            net_IRR_test[( s + sim*k)] = npf.irr(cf_total) * 12
                        else:
                            net_IRR_test[s] = npf.irr(cf_total) * 12


                        cf_in = np.zeros(120)
                        cf_in[0:60] = drawn_cap_total[0:60] - mgm_fee_vector#-paid_int
                        cf_in[60:120] = drawn_cap_total[60:120] - mgm_fee_div
                        cf_out = exit_each_month_120[s, :]
                        cf_total = np.zeros(120)
                        cf_total[0:120] = - cf_in + cf_out
                        gross_IRR[s] = npf.irr(cf_total) * 12

                        if k > 0:
                            gross_IRR_test[(s + sim*k)] = npf.irr(cf_total) * 12
                        else:
                            gross_IRR_test[s] = npf.irr(cf_total) * 12

                        # PAY-OFF SECTION
                        distributions = np.zeros(120)
                        distributions[0:120] = exit_each_month_120[s, :]
                        cum_distribution = np.cumsum(distributions)
                        to_be_returned_pre_hurdle_ = np.ones(120) * cumsum_drawn_cap_div[59]
                        drawn_down_balance_ = np.zeros(120)
                        drawn_down_balance_[0:60] = drawn_cap
                        available_for_hurdle_carry_ = np.zeros(120)
                        returned_pre_hurdle_carry_ = np.zeros(120)
                        for i in range(120):
                            if distributions[i] >= to_be_returned_pre_hurdle_[i]:
                                returned_pre_hurdle_carry_[i] = to_be_returned_pre_hurdle_[i]
                                drawn_down_balance_[i] = 0
                                available_for_hurdle_carry_[i] = distributions[i] - to_be_returned_pre_hurdle_[i]
                                if i < 119:
                                    to_be_returned_pre_hurdle_[i + 1] = 0
                            elif distributions[i] > 0 and distributions[i] < to_be_returned_pre_hurdle_[i]:
                                returned_pre_hurdle_carry_[i] = distributions[i]
                                if i < 119:
                                    to_be_returned_pre_hurdle_[i + 1] = to_be_returned_pre_hurdle_[i] - returned_pre_hurdle_carry_[
                                        i]
                                    drawn_down_balance_[i] = 0

                            elif distributions[i] == 0 and i < 119:
                                to_be_returned_pre_hurdle_[i + 1] = to_be_returned_pre_hurdle_[i]

                        cum_av_for_hurdle_carry_ = np.cumsum(available_for_hurdle_carry_)

                        hurdle_rate = 0.08
                        hurdle_rel_to_period = np.zeros(120)
                        hurdle_rel_to_period[0:60] = drawn_cap * hurdle_rate
                        tot_hurdle_outstanding = np.cumsum(hurdle_rel_to_period)
                        tot_av_for_hurdle_carry = available_for_hurdle_carry_

                        hur_paid_to_LP = np.zeros(120)
                        ret_av_for_carry = np.zeros(120)

                        for i in range(120):
                            if tot_hurdle_outstanding[i] <= tot_av_for_hurdle_carry[i] and tot_av_for_hurdle_carry[i] != 0:
                                hur_paid_to_LP[i] = tot_hurdle_outstanding[i]
                                ret_av_for_carry[i] = tot_av_for_hurdle_carry[i] - tot_hurdle_outstanding[i]

                                if i < 119:
                                    tot_hurdle_outstanding[i + 1] = 0
                                    tot_hurdle_outstanding[i:120] = 0


                            elif (tot_av_for_hurdle_carry[i] > 0) and (tot_hurdle_outstanding[i] > \
                                                                       tot_av_for_hurdle_carry[i]):
                                hur_paid_to_LP[i] = tot_av_for_hurdle_carry[i]
                                ret_av_for_carry[i] = 0

                                if i < 119:
                                    tot_hurdle_outstanding[i + 1] = tot_hurdle_outstanding[i] - hur_paid_to_LP[i]

                            if hur_paid_to_LP[i] == 0 and i < 119 and i > 59:
                                tot_hurdle_outstanding[i + 1] = tot_hurdle_outstanding[i]

                        cum_paid_hurdle = np.cumsum(hur_paid_to_LP)
                        cum_ret_carry = np.cumsum(ret_av_for_carry)

                        # CARRY TIER 1

                        rate_12 = 0.12
                        net_catchup_rel_to_per = np.zeros(120)
                        net_catchup_rel_to_per[0:60] = drawn_cap * (1 + rate_12) - drawn_cap * (1 + hurdle_rate)
                        tot_carry_outstanding = np.cumsum(net_catchup_rel_to_per)
                        catchup_balance = np.zeros(120)
                        catchup_balance[0:60] = tot_carry_outstanding[0:60]
                        catchup_balance[60:120] = tot_carry_outstanding[60:120] - ret_av_for_carry[60:120]
                        paid_carry = np.zeros(120)

                        for i in range(120):
                            if (ret_av_for_carry[i] > 0) and (ret_av_for_carry[i] < tot_carry_outstanding[i]):
                                catchup_balance[i] = tot_carry_outstanding[i] - ret_av_for_carry[i]
                                paid_carry[i] = ret_av_for_carry[i]

                                if i < 119:
                                    ret_av_for_carry[i + 1] = ret_av_for_carry[i] - paid_carry[i]
                                    tot_carry_outstanding[i + 1:120] = catchup_balance[i]
                                    catchup_balance[i + 1:120] = catchup_balance[i]

                            elif (ret_av_for_carry[i] > 0) and (ret_av_for_carry[i] > tot_carry_outstanding[i]):
                                catchup_balance[i:120] = 0
                                paid_carry[i] = tot_carry_outstanding[i]
                                if i < 119:
                                    tot_carry_outstanding[i + 1:120] = 0
                                    catchup_balance[i + 1] = 0

                        tot_paid_carry = np.cumsum(paid_carry)
                        carry_to_LP = 0.4 * paid_carry
                        carry_to_GP = 0.6 * paid_carry

                        tier_1_GP[s] = np.sum(carry_to_GP)
                        tier_1_LP[s] = np.sum(carry_to_LP)

                        ##### CARRY TIER 2
                        # total_tier_2 = np.cumsum(ret_av_for_carry) - paid_carry
                        total_tier_2 = ret_av_for_carry - paid_carry
                        tier_2_LP[s] = np.sum(0.8 * total_tier_2)
                        tier_2_GP[s] = np.sum(0.2 * total_tier_2)

                        RM[s] = (total_exit - (tier_1_GP[s] + tier_2_GP[s])) / cumsum_drawn_cap_div[59]


                    df_hurdle = pd.DataFrame(
                        [hurdle_rel_to_period, tot_hurdle_outstanding, hur_paid_to_LP, cum_paid_hurdle, ret_av_for_carry
                            , cum_ret_carry],
                        index=['Hurdle related to period', 'Total hurdle outstanding', 'Hurdple paid to LP'
                            , 'Cumulative hurdle paid', 'Return available for carry',
                               'Cumulative return to carry'], columns=kolumner)

                    # LAYOUT : HURDLE TABLE NO LOAN
                    st.markdown('##')
                    st.subheader('Example of numbers from one simulation')

                    st.write('Investment developement')
                    #if st.checkbox('Show investment development', key='inv_development' + str(k)):
                    st.write(pd.DataFrame(simulated_investments, index=rader, columns=kolumner))

                    df_catch_up = pd.DataFrame([net_catchup_rel_to_per, tot_carry_outstanding, catchup_balance, paid_carry,
                                                tot_paid_carry, carry_to_LP, carry_to_GP],
                                               index=['Net catch-up related to period', 'Total carry outstanding',
                                                      'Catch-up balance',
                                                      'Paid carry', 'Cumulative paid carry', 'Carry to LP', 'Carry to GP']
                                               , columns=kolumner)

                    # LAYOUT : TIER 1 TABLE NO LOAN

                    total_tier_2 = ret_av_for_carry - paid_carry
                    example_tier_2_LP = 0.8 * total_tier_2
                    example_tier_2_GP = 0.2 * total_tier_2

                    df_tier_2 = pd.DataFrame([total_tier_2, example_tier_2_LP, example_tier_2_GP], index=['Total', 'To LP', 'To GP']
                                             , columns=kolumner)

                    # LAYOUT : TIER 2 TABLE NO LOAN

                    st.markdown('##')
                    st.subheader('Payoff for each tier')
                    #st.markdown('#')
                   # if st.checkbox('Show payoff tables for each tier',key='tier_tables'+str(k)):
                    st.markdown('#')
                    st.write('Hurdle')
                    st.write(df_hurdle)
                    st.write('Catch-up TIER 1')
                    st.write(df_catch_up)
                    st.write('Profit sharing TIER 2')
                    st.write(df_tier_2)
                    st.markdown('#')

                    min_MOIC = min(MOIC);
                    max_MOIC = max(MOIC);
                    mean_MOIC = stat.mean(MOIC);
                    med_MOIC = stat.median(MOIC);
                    var_MOIC = stat.variance(MOIC);
                    std_MOIC = stat.stdev(MOIC);
                    per_MOIC = np.percentile(MOIC, [25, 50, 75]);
                    per_25_MOIC = per_MOIC[0];
                    per_50_MOIC = per_MOIC[1];
                    per_75_MOIC = per_MOIC[2];

                    nan_array = np.isnan(IRR)
                    not_nan_array = ~ nan_array
                    IRR = IRR[not_nan_array]

                    min_IRR = min(IRR);
                    max_IRR = max(IRR);
                    mean_IRR = stat.mean(IRR);
                    med_IRR = stat.median(IRR);
                    var_IRR = stat.variance(IRR);
                    per_IRR = np.percentile(IRR, [25, 50, 75]);
                    per_25_IRR = per_IRR[0];
                    per_50_IRR = per_IRR[1];
                    per_75_IRR = per_IRR[2];

                    gross_min_IRR = min(gross_IRR);
                    gross_max_IRR = max(gross_IRR);
                    mean_gross_IRR = stat.mean(gross_IRR);
                    med_gross_IRR = stat.median(gross_IRR);
                    var_gross_IRR = stat.variance(gross_IRR);
                    per_gross_IRR = np.percentile(gross_IRR, [25, 50, 75]);
                    per_25_gross_IRR = per_gross_IRR[0];
                    per_50_gross_IRR = per_gross_IRR[1];
                    per_75_gross_IRR = per_gross_IRR[2];


                    # CODE : STATISTICS ON RM : REALIZATION MULTIPLE
                    min_RM = min(RM);
                    max_RM = max(RM);
                    mean_RM = stat.mean(RM);
                    med_RM = stat.median(RM);
                    var_RM = stat.variance(RM);
                    std_RM = stat.stdev(RM);
                    per_RM = np.percentile(RM, [25, 50, 75]);
                    per_25_RM = per_RM[0];
                    per_50_RM = per_RM[1];
                    per_75_RM = per_RM[2];

                    df_performance = pd.DataFrame(data=[[min_IRR, max_IRR, mean_IRR, med_IRR, var_IRR, per_25_IRR, per_75_IRR],
                                                        [gross_min_IRR, gross_max_IRR, mean_gross_IRR, med_gross_IRR,
                                                         var_gross_IRR, per_25_gross_IRR, per_75_gross_IRR],
                                                        [min_MOIC, max_MOIC, mean_MOIC, med_MOIC, var_MOIC, per_25_MOIC, per_75_MOIC],
                                                        [min_RM, max_RM, mean_RM, med_RM, var_RM, per_25_RM, per_75_RM]],
                                                  columns=['Min', 'Max', 'Mean', 'Median', 'Variance', '25% Percentile',
                                                           '75% Percentile'],
                                                  index=['Net-IRR', 'Gross-IRR', 'MOIC', 'DPI'])

                    st.markdown('##')
                    st.markdown('#')
                    st.header('Summary statistics')
                    st.subheader('Performance Statistics')
                    st.write(np.transpose(df_performance))

                    # CODE : STATISTICS ON LP VS GP GAIN
                    LP = tier_1_LP + tier_2_LP
                    GP = tier_1_GP + tier_2_GP

                    if k > 0:
                        lp_tier_1[(sim*k):(sim*k)+sim] = tier_1_LP
                        gp_tier_1[(sim*k):(sim*k)+sim]  = tier_1_GP
                        lp_tier_2[(sim*k):(sim*k)+sim]  = tier_2_LP
                        gp_tier_2[(sim*k):(sim*k)+sim]  = tier_2_GP
                        lp_test[(sim*k):(sim*k)+sim]  = LP
                        gp_test[(sim*k):(sim*k)+sim]  = GP
                    else:
                        lp_tier_1[0:sim] = tier_1_LP
                        gp_tier_1[0:sim] = tier_1_GP
                        lp_tier_2[0:sim] = tier_2_LP
                        gp_tier_2[0:sim] = tier_2_GP
                        lp_test[0:sim] = LP
                        gp_test[0:sim] = GP

                    min_LP = min(LP);
                    max_LP = max(LP);
                    mean_LP = stat.mean(LP);
                    med_LP = stat.median(LP);
                    std_LP = np.sqrt(stat.variance(LP));
                    per_LP = np.percentile(LP, [25, 50, 75]);
                    per_25_LP = per_LP[0];
                    per_50_LP = per_LP[1];
                    per_75_LP = per_LP[2];

                    min_GP = min(GP);
                    max_GP = max(GP);
                    mean_GP = stat.mean(GP);
                    med_GP = stat.median(GP);
                    std_GP = np.sqrt(stat.variance(GP));
                    per_GP = np.percentile(GP, [25, 50, 75]);
                    per_25_GP = per_GP[0];
                    per_50_GP = per_GP[1];
                    per_75_GP = per_GP[2];



                    st.markdown('##')
                    st.subheader('Payoff Statistics')
                    df_payoff = pd.DataFrame(data=[[min_LP, max_LP, mean_LP, med_LP, std_LP, per_25_LP, per_75_LP],
                                                   [min_GP, max_GP, mean_GP, med_GP, std_GP, per_25_GP, per_75_GP]],
                                             columns=['Min', 'Max', 'Mean', 'Median', 'Standard deviation', '25% Percentile',
                                                      '75% Percentile'],
                                             index=['To LP', 'To GP'])

                # Create latex code:
               #     for j in range(6):
               #         st.write('&',df_payoff.iloc[0,j],'&',df_payoff.iloc[1,j], '\\','\\')

                    st.write(np.transpose(df_payoff))

                    # CODE : COUNT IRR BRACKETS
                    a = b = c = d = e = f = g = h = j = k_ = l = m = n = o = p = q = r = 0
                    for i in range(len(IRR)):
                        if IRR[i] < 0.08:
                            a += 1
                        elif 0.08 <= IRR[i] < 0.10:
                            b += 1
                        elif 0.10 <= IRR[i] < 0.12:
                            c += 1
                        elif 0.12 <= IRR[i] < 0.14:
                            d += 1
                        elif 0.14 <= IRR[i] < 0.16:
                            e += 1
                        elif 0.16 <= IRR[i] < 0.18:
                            f += 1
                        elif 0.18 <= IRR[i] < 0.20:
                            g += 1
                        elif 0.20 <= IRR[i] < 0.22:
                            h += 1
                        elif 0.22 <= IRR[i] < 0.24:
                            i += 1
                        elif 0.24 <= IRR[i] < 0.26:
                            j += 1
                        elif 0.26 <= IRR[i] < 0.28:
                            k_ += 1
                        elif 0.28 <= IRR[i] < 0.30:
                            l += 1
                        elif 0.30 <= IRR[i] < 0.32:
                            m += 1
                        elif 0.32 <= IRR[i] < 0.34:
                            n += 1
                        elif 0.34 <= IRR[i] < 0.36:
                            o += 1
                        elif 0.36 <= IRR[i] < 0.38:
                            p += 1
                        elif 0.38 <= IRR[i] < 0.40:
                            q += 1
                        else:
                            r += 1

                    IRR_intervals = ['  IRR < 8%', ' 8% <= IRR < 10%', '10% <= IRR < 12%', '12% <= IRR < 14%', '14% <= IRR < 16%',
                                     '16% <= IRR < 18%', '18% <= IRR < 20%', '20% <= IRR < 22%', '22% <= IRR < 24%', '24% <= IRR < 26%',
                                     '26% <= IRR < 28%', '28% <= IRR < 30%','30% <= IRR < 32%','32% <= IRR < 34%','34% <= IRR < 36%',
                                     '36% <= IRR < 38%','38% <= IRR < 40%','IRR => 40%']

                    brackets_IRR = pd.DataFrame([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r], index=IRR_intervals,
                                                columns=['Net-IRR - Count'])

                    a = b = c = d = e = f = g = h = i = j = k_ = l = m = n = o = p = q = r = 0
                    for i in range(len(gross_IRR)):
                        if gross_IRR[i] < 0.08:
                            a += 1
                        elif 0.08 <= gross_IRR[i] < 0.10:
                            b += 1
                        elif 0.10 <= gross_IRR[i] < 0.12:
                            c += 1
                        elif 0.12 <= gross_IRR[i] < 0.14:
                            d += 1
                        elif 0.14 <= gross_IRR[i] < 0.16:
                            e += 1
                        elif 0.16 <= gross_IRR[i] < 0.18:
                            f += 1
                        elif 0.18 <= gross_IRR[i] < 0.20:
                            g += 1
                        elif 0.20 <= gross_IRR[i] < 0.22:
                            h += 1
                        elif 0.22 <= gross_IRR[i] < 0.24:
                            i += 1
                        elif 0.24 <= gross_IRR[i] < 0.26:
                            j += 1
                        elif 0.26 <= gross_IRR[i] < 0.28:
                            k_ += 1
                        elif 0.28 <= gross_IRR[i] < 0.30:
                            l += 1
                        elif 0.30 <= gross_IRR[i] < 0.32:
                            m += 1
                        elif 0.32 <= gross_IRR[i] < 0.34:
                            n += 1
                        elif 0.34 <= gross_IRR[i] < 0.36:
                            o += 1
                        elif 0.36 <= gross_IRR[i] < 0.38:
                            p += 1
                        elif 0.38 <= gross_IRR[i] < 0.40:
                            q += 1
                        else:
                             r+= 1

                    brackets_gross_IRR = pd.DataFrame([a, b, c, d, e, f, g, h, i, j, k_, l, m, n, o, p, q, r], index=IRR_intervals,
                                                      columns=['Gross-IRR - Count'])

                    # LAYOUT : IRR BRACKET ANALYSIS TABLE
                    result_2 = [brackets_IRR, brackets_gross_IRR]


            # Create latex code:
          #          for j in range(18):
           #             st.write('&',(pd.concat(result_2, axis=1)).iloc[j,0],'&',(pd.concat(result_2, axis=1)).iloc[j,1], '\\','\\')


                    st.markdown('#')

                    # CREATE BRACKETS MEAN

                    df_merged = np.transpose(pd.DataFrame(data=[GP, IRR], index=['GP', 'Net-IRR']))
                    mean_vec = np.zeros(len(np.arange(8, 42, 2))+1)
                    j = 0
                    for i in np.arange(6, 42, 2):
                        if i == 40:
                            data = df_merged[
                                df_merged['Net-IRR'].between((i / 100), max(df_merged['Net-IRR']), inclusive=True)]
                        elif i == 6:
                            data = df_merged[
                                df_merged['Net-IRR'].between(min(df_merged['Net-IRR']), ((i+2) / 100), inclusive=True)]

                        else:
                            data = df_merged[
                                df_merged['Net-IRR'].between((i / 100), ((i + 2) / 100), inclusive=True)]
                        mean_vec[j] = np.mean(data['GP'])
                        j = j + 1

                    mean_vec = (pd.DataFrame(mean_vec, columns=['Net-IRR - Payoff to GP'])).fillna(0)

                    df_merged_LP = np.transpose(pd.DataFrame(data=[LP, IRR], index=['LP', 'Net-IRR']))
                    mean_vec_LP = np.zeros(len(np.arange(8, 42, 2))+1)
                    j = 0

                    for i in np.arange(6, 42, 2):
                        if i == 40:
                            data_LP = df_merged_LP[
                                df_merged_LP['Net-IRR'].between((i / 100), max(df_merged_LP['Net-IRR']), inclusive=True)]
                        elif i == 6:
                            data_LP = df_merged_LP[
                                df_merged_LP['Net-IRR'].between(min(df_merged_LP['Net-IRR']), ((i+2) / 100), inclusive=True)]
                        else:
                            data_LP = df_merged_LP[
                                df_merged_LP['Net-IRR'].between((i / 100), ((i + 2) / 100), inclusive=True)]
                        mean_vec_LP[j] = np.mean(data_LP['LP'])
                        j = j + 1

                    mean_vec_LP = (pd.DataFrame(mean_vec_LP, columns=['Net-IRR - Payoff to LP'])).fillna(0)

                    df = pd.concat([mean_vec, mean_vec_LP], axis=1)
                    df.index = IRR_intervals

                    st.markdown('##')

            # Create Latex code:
            #        for j in range(18):
            #            st.write('&',df.iloc[j,0],'&',df.iloc[j,1], '\\','\\')
                    # st.line_chart(df)

                    # CREATE BRACKETS MEAN  - GROSS-IRR
                    df_merged_gross_2 = np.transpose(pd.DataFrame(data=[tier_2_GP, gross_IRR], index=['Tier 2 - GP', 'Gross-IRR']))
                    df_merged_gross_1 = np.transpose(
                        pd.DataFrame(data=[tier_1_GP, gross_IRR], index=['Tier 1 - GP', 'Gross-IRR']))
                    df_merged_gross = np.transpose(pd.DataFrame(data=[GP, gross_IRR], index=['GP', 'Gross-IRR']))
                    mean_vec_gross = np.zeros(len(np.arange(6, 42, 2)))
                    mean_vec_gross_1 = np.zeros(len(np.arange(6, 42, 2)))
                    mean_vec_gross_2 = np.zeros(len(np.arange(6, 42, 2)))
                    j = 0
                    for i in np.arange(6, 42, 2):
                        if i == 40:
                            data_GP_gross = df_merged_gross[
                                df_merged_gross['Gross-IRR'].between((i / 100), max(df_merged_gross['Gross-IRR']), inclusive=True)]
                            data_GP_gross_2 = df_merged_gross_2[
                                df_merged_gross_2['Gross-IRR'].between((i / 100), max(df_merged_gross_2['Gross-IRR']),
                                                                     inclusive=True)]
                            data_GP_gross_1 = df_merged_gross_1[
                                df_merged_gross_1['Gross-IRR'].between((i / 100), max(df_merged_gross_1['Gross-IRR']),
                                                                       inclusive=True)]
                        elif i == 6:
                            #st.write(i)
                            data_GP_gross = df_merged_gross[
                                df_merged_gross['Gross-IRR'].between(min(df_merged_gross['Gross-IRR']), ((i+2) / 100), inclusive=True)]
                            data_GP_gross_2 = df_merged_gross_2[
                                df_merged_gross_2['Gross-IRR'].between(min(df_merged_gross_2['Gross-IRR']), ((i + 2) / 100),
                                                                     inclusive=True)]
                            data_GP_gross_1 = df_merged_gross_1[
                                df_merged_gross_1['Gross-IRR'].between(min(df_merged_gross_1['Gross-IRR']),
                                                                       ((i + 2) / 100),
                                                                       inclusive=True)]
                        else:
                            data_GP_gross = df_merged_gross[
                                df_merged_gross['Gross-IRR'].between((i / 100), ((i + 2) / 100), inclusive=True)]
                            data_GP_gross_2 = df_merged_gross_2[
                                df_merged_gross_2['Gross-IRR'].between((i / 100), ((i + 2) / 100), inclusive=True)]
                            data_GP_gross_1 = df_merged_gross_1[
                                df_merged_gross_1['Gross-IRR'].between((i / 100), ((i + 2) / 100), inclusive=True)]
                        mean_vec_gross[j] = np.mean(data_GP_gross['GP'])
                        mean_vec_gross_2[j] = np.mean(data_GP_gross_2['Tier 2 - GP'])
                        mean_vec_gross_1[j] = np.mean(data_GP_gross_1['Tier 1 - GP'])
                        j = j + 1


                    if k>0:
                        gp_gross_bracket[18*k:(18*k+18)] = mean_vec_gross
                        gp_gross_bracket_1[18 * k:(18 * k + 18)] = mean_vec_gross_1
                        gp_gross_bracket_2[18*k:(18 * k + 18)] = mean_vec_gross_2

                    else:
                        gp_gross_bracket[0:18] = mean_vec_gross
                        gp_gross_bracket_1[0:18] = mean_vec_gross_1
                        gp_gross_bracket_2[0:18] = mean_vec_gross_2


                    mean_vec_gross = (pd.DataFrame(mean_vec_gross, columns=['Gross-IRR -  Payoff to GP'])).fillna(0)
                    mean_vec_gross_2 = (pd.DataFrame(mean_vec_gross_2, columns=['Gross-IRR -  Payoff to GP'])).fillna(0)

                    df_merged_LP_gross = np.transpose(pd.DataFrame(data=[LP, gross_IRR], index=['LP', 'Gross-IRR']))
                    mean_vec_LP_gross = np.zeros(18)
                    j = 0
                    for i in np.arange(6, 42, 2):
                        if i == 40:
                            data_LP_gross = df_merged_LP_gross[
                                df_merged_LP_gross['Gross-IRR'].between((i / 100), max(df_merged_LP_gross['Gross-IRR']), inclusive=True)]
                        elif i == 6:
                            data_LP_gross = df_merged_LP_gross[
                                df_merged_LP_gross['Gross-IRR'].between(min(df_merged_LP_gross['Gross-IRR']), ((i+2) / 100), inclusive=True)]
                        else:
                            data_LP_gross = df_merged_LP_gross[
                                df_merged_LP_gross['Gross-IRR'].between((i / 100), ((i + 2) / 100), inclusive=True)]
                        mean_vec_LP_gross[j] = np.mean(data_LP_gross['LP'])
                        j = j + 1

                    if k>0:
                        lp_gross_bracket[18*k:(18*k+18)] = mean_vec_LP_gross
                    else:
                        lp_gross_bracket[0:18] = mean_vec_LP_gross


                    mean_vec_LP_gross = (pd.DataFrame(mean_vec_LP_gross, columns=['Gross-IRR -  Payoff to LP'])).fillna(0)
                    df_gross = pd.concat([mean_vec_gross, mean_vec_LP_gross], axis=1)
                    df_gross.index = IRR_intervals


                    st.subheader('IRR distribution')
                    fig, ax = plt.subplots()
                    ax.hist([IRR, gross_IRR], alpha=0.8, label=([ 'Net-IRR','Gross-IRR']))#, bins=100)
                    ax.legend(loc='upper right')
                    st.pyplot(fig)

                st.markdown('##')
                st.markdown('##')


            net_irr_comp = np.zeros((len(fin_stra),sim))
            gross_irr_comp = np.zeros((len(fin_stra),sim))
            lp_comp = np.zeros((len(fin_stra),sim)); gp_comp = np.zeros((len(fin_stra),sim))
            lp_tier_2_ = np.zeros((len(fin_stra),sim)); gp_tier_2_ = np.zeros((len(fin_stra),sim))

            for i in range(len(fin_stra)):
                net_irr_comp[i,:] = net_IRR_test[i*sim: (i+1)*sim]
                gross_irr_comp[i, :] = gross_IRR_test[i * sim: (i + 1) * sim]
                lp_comp[i, :] = lp_test[i * sim: (i + 1) * sim]
                gp_comp[i, :] = gp_test[i * sim: (i + 1) * sim]
                lp_tier_2_[i, :] = lp_tier_2[i * sim: (i + 1) * sim]
                gp_tier_2_[i, :] = gp_tier_2[i * sim: (i + 1) * sim]



            st.header('Comparison of IRR-distributions')

            st.subheader('Net-IRR distribution')
            fig, ax = plt.subplots()
            ax.hist(np.transpose(net_irr_comp), alpha=0.8, label=(fin_stra))#[fin_stra[0], fin_stra[1]]))  # , bins=100)
            ax.legend(loc='upper right')
            st.pyplot(fig)

            st.subheader('Gross-IRR distribution')
            fig, ax = plt.subplots()
            ax.hist(np.transpose(gross_irr_comp), alpha=0.8, label=([fin_stra[0], fin_stra[1]]))#, bins=100)
            ax.legend(loc='upper right')
            st.pyplot(fig)


            # COMPARISON BETWEEN STRATEGIES
            st.markdown('##')
            st.header('Comparison of Distribution of Returns')

            st.subheader('Return to LP')
            fig, ax = plt.subplots()
            ax.hist(np.transpose(lp_comp), alpha=0.8, label=(fin_stra))#[fin_stra[0], fin_stra[1]]))#, bins=100)
            ax.legend(loc='upper right')
            st.pyplot(fig)

            st.subheader('Return to GP')
            fig, ax = plt.subplots()
            ax.hist(np.transpose(gp_comp), alpha=0.8, label=(fin_stra)) #[fin_stra[0], fin_stra[1]]))#, bins=100)
            ax.legend(loc='upper right')
            st.pyplot(fig)


        # TIER 1 plos
        #    st.subheader('Tier 1 - Return to LP')
        #    fig, ax = plt.subplots()
        #    ax.hist([lp_tier_1_1, lp_tier_1_2], alpha=0.8, label=(fin_str[fin_stra[0], fin_stra[1]]))  # , bins=100)
        #    ax.legend(loc='upper right')
        #    st.pyplot(fig)

         #   st.subheader('Tier 1 - Return to GP')
         #   fig, ax = plt.subplots()
         #   ax.hist([gp_tier_1_1, gp_tier_1_2], alpha=0.8, label=([fin_stra[0], fin_stra[1]]))  # , bins=100)
         #   ax.legend(loc='upper right')
         #   st.pyplot(fig)

            st.subheader('Tier 2 - Profit sharing - Return to LP')
            fig, ax = plt.subplots()
            ax.hist(np.transpose(lp_tier_2_), alpha=0.8, label=(fin_stra))#[fin_stra[0], fin_stra[1]])) # , bins=100)
            ax.legend(loc='upper right')
            st.pyplot(fig)

            st.subheader('Tier 2 - Profit sharing - Return to GP')
            fig, ax = plt.subplots()
            ax.hist(np.transpose(gp_tier_2_), alpha=0.8, label=(fin_stra))#[fin_stra[0], fin_stra[1]])) #, bins=100)
            ax.legend(loc='upper right')
            st.pyplot(fig)


            gp_gross_array = []
            gp_gross_array_1 = []
            gp_gross_array_2 = []
            lp_gross_array = []
            for i in range(len(fin_stra)):
                gp_gross_array.append(gp_gross_bracket[i*18:(1+i)*18])
                gp_gross_array_1.append(gp_gross_bracket_1[i * 18:(1 + i) * 18])
                gp_gross_array_2.append(gp_gross_bracket_2[i*18:(1+i)*18])
                lp_gross_array.append(lp_gross_bracket[i * 18:(1 + i) * 18])

            df_lp_gross_bracket = (pd.DataFrame(data=np.transpose(lp_gross_array),
                                                index=IRR_intervals, columns=(fin_stra))).fillna(0)
            df_gp_gross_bracket = (pd.DataFrame(data=np.transpose(gp_gross_array),
                                                index=IRR_intervals, columns=(fin_stra))).fillna(0)
            df_gp_gross_bracket_1 = (pd.DataFrame(data=np.transpose(gp_gross_array_1),
                                                  index=IRR_intervals, columns=(fin_stra))).fillna(0)
            df_gp_gross_bracket_2 = (pd.DataFrame(data=np.transpose(gp_gross_array_2),
                                                index=IRR_intervals, columns=(fin_stra))).fillna(0)



        # Line charts of Distribution of Returns vs Gross-IRR Brackets
        #    st.subheader('LP - Total Compensation - Bracket')
        #    st.line_chart((df_lp_gross_bracket))
        #    st.subheader('GP - Total Compensation - Bracket')
        #    st.line_chart((df_gp_gross_bracket))
        #    st.subheader('GP - Tier 1 Compensation - Bracket')
        #    st.line_chart((df_gp_gross_bracket_1))
        #    st.subheader('GP - Tier 2 Compensation - Bracket')
        #    st.line_chart((df_gp_gross_bracket_2))










