#!/usr/bin/env python
# coding: utf-8

# # PyCity Schools Analysis
# - As a whole, schools with higher budgets, did not yield better test results. By contrast, schools with higher spending 645-675 per student actually underperformed compared to schools with smaller budgets (585 per student).
# 
# - As a whole, smaller and medium sized schools dramatically out-performed large sized schools on passing math performances (89-91% passing vs 67%).
# 
# - As a whole, charter schools out-performed the public district schools across all metrics. However, more analysis will be required to glean if the effect is due to school practices or the fact that charter schools tend to serve smaller student populations per school.
# 
# 

# In[350]:


# Dependencies and Setup
import pandas as pd

# File to Load (Remember to Change These)
school_data_to_load = "C:/Users/44739/Desktop/schools_complete.csv"
student_data_to_load = "C:/Users/44739/Desktop/students_complete.csv"

# Read School and Student Data File and store into Pandas DataFrames
school_data = pd.read_csv(school_data_to_load)
student_data = pd.read_csv(student_data_to_load)

# Combine the data into a single dataset.  
school_data_complete = pd.merge(student_data, school_data, how="left", on=["school_name", "school_name"])
school_data_complete.head()


# # District Summary

# In[318]:


# Calculate the total number of unique schools
school_count = school_data_complete['school_name'].unique()
total_school_number=len(school_count)

total_school_number


# In[319]:


# Calculate the total number of students
student_count = school_data_complete["student_name"].count()
student_count


# In[320]:


# Calculate the total budget
total_budget = school_data["budget"].sum()
total_budget


# In[321]:


# Calculate the average (mean) math score
average_math_score = school_data_complete["math_score"].mean()
average_math_score


# In[322]:


# Calculate the average (mean) reading score
average_reading_score = school_data_complete["reading_score"].mean()
average_reading_score


# In[323]:


# Use the following to calculate the percentage of students who passed math (math scores greather than or equal to 70)
students_passing_math_count = school_data_complete[(school_data_complete["math_score"] >= 70)].count()["student_name"]
students_passing_math_percentage = students_passing_math_count / float(student_count) * 100
students_passing_math_percentage


# In[324]:


# Calculate the percentage of students who passed reading (hint: look at how the math percentage was calculated)  
students_passing_reading_count = school_data_complete.loc[school_data_complete["reading_score"] >= 70]
students_passing_reading_percentage = students_passing_reading_count = students_passing_reading_count["Student ID"].count()

students_percent_passing_reading = (students_passing_reading_percentage / student_count) * 100
students_percent_passing_reading


# In[325]:


# Use the following to calculate the percentage of students that passed math and reading
passing_math_reading_count = school_data_complete[
    (school_data_complete["math_score"] >= 70) & (school_data_complete["reading_score"] >= 70)
].count()["student_name"]
overall_passing_rate = passing_math_reading_count /  float(student_count) * 100
overall_passing_rate


# In[326]:


# Create a high-level snapshot of the district's key metrics in a DataFrame
district_summary = pd.DataFrame({"Total Schools": total_school_number,"Total Students": f"{student_count:,}",
    "Total Budget": f"${total_budget:,.2f}", "Average Math Score": f"{average_math_score:.6f}",
    "Average Reading Score": f"{average_reading_score:.5f}", "% Passing Math": f"{students_passing_math_percentage:.6f}", 
    "% Passing Reading": f"{students_percent_passing_reading:.6f}", "% Overall Passing": f"{overall_passing_rate: .6f}"}, index=[0])


# Display the DataFrame
district_summary


# # School Summary

# In[327]:


# Use the code provided to select the school type
school_name = school_data_complete.set_index('school_name').groupby(['school_name'])
school_type = school_data.set_index(["school_name"])["type"]


# In[328]:


# Calculate the total student count
total_student_count = school_name['Student ID'].count()


# In[329]:


# Calculate the total school budget and per capita spending
total_school_budget = school_data.set_index('school_name')['budget']
per_student_budget = (school_data.set_index('school_name')['budget']/school_data.set_index('school_name')['size'])


# In[330]:


# Calculate the average test scores
average_math_score = school_name['math_score'].mean()
average_reading_score = school_name['reading_score'].mean()


# In[331]:


# Calculate the number of schools with math scores of 70 or higher
school_passing_math = school_data_complete[school_data_complete['math_score'] >= 70].groupby('school_name')


# In[332]:


# Calculate the number of schools with reading scores of 70 or higher
school_passing_reading = school_data_complete[school_data_complete['reading_score'] >= 70].groupby('school_name')


# In[333]:


# Use the provided code to calculate the schools that passed both math and reading with scores of 70 or higher
passing_math_and_reading = school_data_complete[
    (school_data_complete["reading_score"] >= 70) & (school_data_complete["math_score"] >= 70)].groupby('school_name')['Student ID'] 
                                                                                                                     


# In[334]:


# Use the provided code to calculate the passing rates
per_school_passing_math = school_data_complete[school_data_complete['math_score'] >= 70].groupby('school_name')['Student ID'].count()/total_student_count*100
per_school_passing_reading = school_data_complete[school_data_complete['reading_score'] >= 70].groupby('school_name')['Student ID'].count()/total_student_count*100
overall_passing_rate = school_data_complete[(school_data_complete['reading_score'] >= 70) & (school_data_complete['math_score'] >= 70)].groupby('school_name')['Student ID'].count()/total_student_count*100


# In[335]:


# Create a DataFrame called `per_school_summary` with columns for the calculations above.

per_school_summary = pd.DataFrame({
    "School Type": school_type,
    "Total Students": total_student_count,
    "Per Student Budget": per_student_budget,
    "Total School Budget": total_school_budget,
    "Average Math Score": average_math_score,
    "Average Reading Score": average_reading_score,
    '% Passing Math': per_school_passing_math,
    '% Passing Reading': per_school_passing_reading,
    "% Overall Passing": overall_passing_rate
})


#munging
per_school_summary = per_school_summary[['School Type', 
                          'Total Students', 
                          'Total School Budget', 
                          'Per Student Budget', 
                          'Average Math Score', 
                          'Average Reading Score',
                          '% Passing Math',
                          '% Passing Reading',
                          '% Overall Passing']]


#formatting
per_school_summary.style.format({'Total Students': '{:}',
                          "Total School Budget": "${:,.2f}",
                          "Per Student Budget": "${:.2f}",
                          'Average Math Score': "{:6f}", 
                          'Average Reading Score': "{:6f}", 
                          "% Passing Math": "{:6f}", 
                          "% Passing Reading": "{:6f}"})


# # Highest-Performing Schools (by % Overall Passing)

# In[336]:


# Sort the schools by `% Overall Passing` in descending order and display the top 5 rows.
top_schools = per_school_summary.sort_values("% Overall Passing", ascending = False)
top_schools.head().style.format({'Total Students': '{:}',
                           "Total School Budget": "${:,.2f}", 
                           "Per Student Budget": "${:.2f}", 
                           "% Passing Math": "{:6f}", 
                           "% Passing Reading": "{:6f}", 
                           "% Overall Passing": "{:6f}"})


# # Bottom Performing Schools (By % Overall Passing)

# In[337]:


# Sort the schools by `% Overall Passing` in ascending order and display the top 5 rows.

bottom_schools = per_school_summary.sort_values('% Overall Passing')
bottom_schools.head().style.format({'Total Students': '{:}', 
                       "Total School Budget": "${:,.2f}", 
                       "Per Student Budget": "${:.2f}", 
                       "% Passing Math": "{:6f}", 
                       "% Passing Reading": "{:6f}", 
                       "% Overall Passing": "{:6f}"})



# # Math Scores by Grade

# In[338]:


# Use the code provided to separate the data by grade
# Group by "school_name" and take the mean of each.
# Use the code to select only the `math_score`.

ninth_graders_ds = school_data_complete.loc[school_data_complete["grade"] == "9th"].groupby(["school_name"])["math_score"].mean()
tenth_graders_ds = school_data_complete.loc[school_data_complete["grade"] == "10th"].groupby(["school_name"])["math_score"].mean()
eleventh_graders_ds = school_data_complete.loc[school_data_complete["grade"] == "11th"].groupby(["school_name"])["math_score"].mean()
twelfth_graders_ds = school_data_complete.loc[school_data_complete["grade"] == "12th"].groupby(["school_name"])["math_score"].mean()

# Combine each of the scores above into single DataFrame called `math_scores_by_grade`
math_scores_by_grade_df = pd.DataFrame({"9th": ninth_graders_ds, "10th": tenth_graders_ds, "11th": eleventh_graders_ds, "12th": twelfth_graders_ds})


# Display the DataFrame
math_scores_by_grade_df[["9th", "10th", "11th", "12th"]]


# # Reading Score by Grade

# In[339]:


# Use the code provided to separate the data by grade
# Group by "school_name" and take the mean of each.
# Use the code to select only the `reading_score`.
ninth_graders_ds = school_data_complete.loc[school_data_complete["grade"] == "9th"].groupby(["school_name"])["reading_score"].mean()
tenth_graders_ds = school_data_complete.loc[school_data_complete["grade"] == "10th"].groupby(["school_name"])["reading_score"].mean()
eleventh_graders_ds = school_data_complete.loc[school_data_complete["grade"] == "11th"].groupby(["school_name"])["reading_score"].mean()
twelfth_graders_ds = school_data_complete.loc[school_data_complete["grade"] == "12th"].groupby(["school_name"])["reading_score"].mean()


# Combine each of the scores above into single DataFrame called `reading_scores_by_grade`
reading_scores_by_grade_df = pd.DataFrame({"9th": ninth_graders_ds, "10th": tenth_graders_ds, "11th": eleventh_graders_ds, "12th": twelfth_graders_ds})

# Display the DataFrame
reading_scores_by_grade_df[["9th", "10th", "11th", "12th"]]


# # Scores by School Spending

# In[340]:


# Establish the bins 
spending_bins = [0, 585, 630, 645, 680]
group_names = ["<$585", "$585-630", "$630-645", "$645-680"]


# In[341]:


# Create a copy of the school summary since it has the "Per Student Budget" 
spending_summary_df = per_school_summary


# In[342]:


# Use `pd.cut` to categorize spending based on the bins.
spending_summary_df["Spending Ranges (Per Student)"] = pd.cut(per_student_budget, spending_bins, labels=group_names, right=False)
spending_summary_df

per_school_summary.style.format({'Total Students': '{: }', 
                       "Total School Budget": "${:,.2f}", 
                       "Per Student Budget": "${:.2f}", 
                       "% Passing Math": "{:6f}", 
                       "% Passing Reading": "{:6f}", 
                       "% Overall Passing": "{:6f}"})


# In[343]:


#  Calculate averages for the desired columns. 
spending_math_scores = school_spending_df.groupby(["Spending Ranges (Per Student)"]).mean()["Average Math Score"]
spending_reading_scores = school_spending_df.groupby(["Spending Ranges (Per Student)"]).mean()["Average Reading Score"]
spending_passing_math = school_spending_df.groupby(["Spending Ranges (Per Student)"]).mean()["% Passing Math"]
spending_passing_reading = school_spending_df.groupby(["Spending Ranges (Per Student)"]).mean()["% Passing Reading"]
overall_passing_spending = school_spending_df.groupby(["Spending Ranges (Per Student)"]).mean()["% Overall Passing"]


# In[344]:


# Assemble into DataFrame
spending_summary = pd.DataFrame({"Average Math Score" : spending_math_scores.round(2),
                                 "Average Reading Score": spending_reading_scores.round(2),
                                 "% Passing Math": spending_passing_math.round(2),
                                 "% Passing Reading": spending_passing_reading.round(2),
                                 "% Overall Passing": overall_passing_spending.round(2)})

# Minor data wrangling
spending_summary = spending_summary[["Average Math Score", 
                                     "Average Reading Score", 
                                     "% Passing Math", "% Passing Reading",
                                     "% Overall Passing"]]

# Display results
spending_summary


# # Scores by School Size

# In[345]:


# Establish the bins.
size_bins = [0, 1000, 2000, 5000]
group_names = ["Small (<1000)", "Medium (1000-2000)", "Large (2000-5000)"]


# In[346]:


# Categorize the spending based on the bins
# Use `pd.cut` on the "Total Students" column of the `per_school_summary` DataFrame.

per_school_summary["School Size"] = pd.cut(per_school_summary["Total Students"], size_bins, labels=group_names, right=False)
per_school_summary

per_school_summary.style.format({'Total Students': '{: }', 
                       "Total School Budget": "${:,.2f}", 
                       "Per Student Budget": "${:.2f}", 
                       "% Passing Math": "{:6f}", 
                       "% Passing Reading": "{:6f}", 
                       "% Overall Passing": "{:6f}"})


# In[347]:


# Calculate averages for the desired columns. 
size_math_scores = per_school_summary.groupby(["School Size"]).mean()["Average Math Score"]
size_reading_scores = per_school_summary.groupby(["School Size"]).mean()["Average Reading Score"]
size_passing_math = per_school_summary.groupby(["School Size"]).mean()["% Passing Math"]
size_passing_reading = per_school_summary.groupby(["School Size"]).mean()["% Passing Reading"]
size_overall_passing = per_school_summary.groupby(["School Size"]).mean()["% Overall Passing"]


# In[348]:


# Create a DataFrame called `size_summary` that breaks down school performance based on school size (small, medium, or large).
# Use the scores above to create a new DataFrame called `size_summary`
size_summary = pd.DataFrame({"Average Math Score" : size_math_scores,
                             "Average Reading Score": size_reading_scores,
                             "% Passing Math": size_passing_math,
                             "% Passing Reading": size_passing_reading,
                             "% Overall Passing": size_overall_passing})

# Minor data wrangling
size_summary = size_summary[["Average Math Score", 
                             "Average Reading Score", 
                             "% Passing Math", "% Passing Reading",
                             "% Overall Passing"]]

# Display results
size_summary


# # Scores by School Type

# In[349]:


# Group the per_school_summary DataFrame by "School Type" and average the results.
type_math_scores = per_school_summary.groupby(["School Type"]).mean()["Average Math Score"]
type_reading_scores = per_school_summary.groupby(["School Type"]).mean()["Average Reading Score"]
type_passing_math = per_school_summary.groupby(["School Type"]).mean()["% Passing Math"]
type_passing_reading = per_school_summary.groupby(["School Type"]).mean()["% Passing Reading"]
type_overall_passing = per_school_summary.groupby(["School Type"]).mean()["% Overall Passing"]

# Use the code provided to select new column data
type_summary = pd.DataFrame({"Average Math Score":type_math_scores,
"Average Reading Score":type_reading_scores,
"% Passing Math":type_passing_math,
"% Passing Reading":type_passing_reading,
"% Overall Passing":type_overall_passing})

# Display results
type_summary

