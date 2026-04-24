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

impaired = active[active["days_past_due"] > 0]

impaired_rate = impaired["balance"].sum() / active["balance"].sum()

print(f"Impaired Rate: {impaired_rate:.2%}")

#Average Arrears per Impaired Account
avg_arrears = impaired["balance"].sum() / impaired.shape[0] if impaired.shape[0] > 0 else 0
print(f"Average Arrears per Impaired Account: KES {avg_arrears:,.2f}")

#Default Rate
default_rate = impaired[impaired["days_past_due"] >= 90]["balance"].sum() / active["balance"].sum()
print(f"Default Rate: {default_rate:.2%}")

#NPE Rate
npe_rate = impaired[impaired["days_past_due"] >= 30]["balance"].sum() / credit["balance"].sum()
print(f"Non-Performing Exposure (NPE) Rate: {npe_rate:.2%}")

#--------------------Visualization-----------------

#NPE Rate Bar chart monthly
npe_rate_monthly = credit.groupby('date').apply(lambda x: x[x['days_past_due'] >= 30]['balance'].sum() / x['balance'].sum())
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

