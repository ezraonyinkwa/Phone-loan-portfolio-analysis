#---------------Portfolio Health-----------------
#PAR Rate 
par_30 = credit[credit['days_past_due'] >= 30]['balance'].sum()/credit['balance'].sum()
par_60 = credit[credit['days_past_due']>=60]['balance'].sum()/credit['balance'].sum()
par_90 = credit[credit['days_past_due']>=90]['balance'].sum()/credit['balance'].sum()

print(f"Portfolio at Risk (PAR) - 30 days: {par_30:.2%}")
print(f"Portfolio at Risk (PAR) - 60 days: {par_60:.2%}")
print(f"Portfolio at Risk (PAR) - 90 days: {par_90:.2%}")

#Impaired Rate
credit["impaired_flag"] = credit["days_past_due"] > 0

#Define denominator for impaired rate calculation
active = credit[credit["balance"] > 0]

impaired = active[active["days_past_due"] > 30]

impaired_rate = impaired["balance"].sum() / active["balance"].sum()

print(f"Impaired Rate: {impaired_rate:.2%}")

#Average Arrears per Impaired Account
avg_arrears = impaired["balance"].sum() / impaired.shape[0] if impaired.shape[0] > 0 else 0
print(f"Average Arrears per Impaired Account: KES {avg_arrears:,.2f}")

#Default Rate
default_rate = impaired[impaired["days_past_due"] >= 60]["balance"].sum() / active["balance"].sum()
print(f"Default Rate: {default_rate:.2%}")

#NPE Rate whole year
npe_rate = impaired[impaired["days_past_due"] >= 90]["balance"].sum() / credit["balance"].sum()
print(f"Non-Performing Exposure (NPE) Rate: {npe_rate:.2%}")
#NPE Rate Average
npe_rate_avg = credit.groupby('date').apply(lambda x: x[x['days_past_due'] >= 90]['balance'].sum() / x['balance'].sum()).mean() 
print(f"Average Non-Performing Exposure (NPE) Rate: {npe_rate_avg:.2%}")

#--------------------Visualization-----------------

#NPE Rate Bar chart monthly
npe_rate_monthly = credit.groupby('date').apply(lambda x: x[x['days_past_due'] >= 90]['balance'].sum() / x['balance'].sum())
npe_rate_monthly.plot(kind='line', figsize=(10, 6))
plt.title('Monthly Non-Performing Exposure (NPE) Rate')
plt.xlabel('Snapshot Date')
plt.ylabel('NPE Rate')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()  

#Default Rate Bar chart monthly
default_rate_monthly = credit.groupby('date').apply(lambda x: x[x['days_past_due'] >= 90]['balance'].sum() / x['balance'].sum())
default_rate_monthly.plot(kind='line', figsize=(10, 6))
plt.title('Monthly Default Rate Trend')
plt.xlabel('Snapshot Date')
plt.ylabel('Default Rate')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()  

#PAR Rate Bar chart monthly
par_30_monthly = credit.groupby('date').apply(lambda x: x[x['days_past_due'] >= 60]['balance'].sum() / x['balance'].sum())
par_30_monthly.plot(kind='line', figsize=(10, 6))
plt.title('Monthly Portfolio at Risk (PAR) - 30 days')
plt.xlabel('Snapshot Date')
plt.ylabel('PAR Rate')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()  

#NPE Rate by Age Group
#Merging the customer DOB dataset with the credit dataset to get the age group for each customer in the credit dataset
credit_with_age = credit.merge(customer_dob[['loan_id', 'age_group']], on='loan_id', how='left')    

npe_by_age_group = credit_with_age.groupby('age_group').apply(lambda x: x[x['days_past_due'] >= 30]['balance'].sum() / x['balance'].sum())
npe_by_age_group.plot(kind='bar', figsize=(10, 6))
plt.title('Non-Performing Exposure (NPE) Rate by Age Group')
plt.xlabel('Age Group')
plt.ylabel('NPE Rate')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#-------------------Credit Outcomes × Customer Experience-------------------------------
#nps score calculation column
nps['nps_score'] = nps['have_you_ever_experienced_a_delay_in_your_payment_reflecting_in_your_mophones_account?'].map({'Yes': 1, 'No': 0})
#Join NPS dataset with the credit dataset on the loan_id column to analyze the relationship between customer experience and credit outcomes
credit_nps = credit.merge(nps[['loan_id', 'nps_score']], on='loan_id', how='left')

#correlation between NPS and Default Rate by month
nps_monthly = credit_nps.groupby('date')['nps_score'].mean()
default_rate_monthly = credit_nps.groupby('date').apply(lambda x: x[x['days_past_due'] >= 90]['balance'].sum() / x['balance'].sum())
correlation = nps_monthly.corr(default_rate_monthly)
print(f"Correlation between NPS and Default Rate: {correlation:.2f}")

#Is there arelationship between credit performance (e.g. arrears,default, account status) and customer satisfaction.
credit_nps['arrears_status'] = credit_nps['days_past_due'] > 0
correlation_arrears_nps = credit_nps['arrears_status'].corr(credit_nps['nps_score'])
print(f"Correlation between Arrears Status and NPS Score: {correlation_arrears_nps:.2f}") 

#Overall customer satisfaction score
overall_nps_score = credit_nps['nps_score'].mean()*100
print(f"Overall NPS Score: {overall_nps_score:.2f}%")

#Correlation between phone pricing and customer satisfaction
#Merging the sales details dataset with the credit_nps dataset to get the phone pricing for each customer in the credit_nps dataset
credit_nps_sales = credit_nps.merge(sales_details[['loan_id', 'loan_price']], on='loan_id', how='left')
correlation_price_nps = credit_nps_sales['loan_price'].corr(credit_nps_sales['nps_score'])
print(f"Correlation between Loan Price and NPS Score: {correlation_price_nps:.2f}")    


#Tension between collections effectiveness and customer experience
collections_effectiveness = credit_nps.groupby('date').apply(lambda x: x[x['days_past_due'] >= 30]['balance'].sum() / x['balance'].sum())

print("Collections Effectiveness (PAR Rate) and Average NPS Score by Month:")
collections_nps = pd.DataFrame({
    'Collections Effectiveness (PAR Rate)': collections_effectiveness,
    'Average NPS Score': nps_monthly
})
print(collections_nps)

#Bar chart to show the relationship between collections effectiveness and customer experience
collections_nps.plot(kind='bar', figsize=(10, 6))
plt.title('Collections Effectiveness (PAR Rate) and Average NPS Score by Month')
plt.xlabel('Snapshot Date')
plt.ylabel('Value')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()




