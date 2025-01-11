from rouge_score import rouge_scorer

rs = rouge_scorer.RougeScorer(['rouge1'], use_stemmer=True)

"""
The answer is 20%

sales
sales department
"""


"""
Generate a test set:
Need a list of tax codes or %vats. e.g
[20,19.5,25,20,25,9]
Plus a list of categories
e.g.['sales','customer', ...]
These are just for constructing the test set
Then with these construct a series of invoices using a METHOD (manual, gpt etc).
For example a 'sales' category invoice which uses vat level 20%
A 'sales' category invoice which uses VAT level '19.5' 
A 'cusomter' category invoice which use... etc
Now - you have the answers already for this test set.
So feed it into your system and do the rouge, not with the invoice and the VAT or the invoice and the category,
but between the test set VAT and the output VAT, and the test set category and the output category.
So if you input the invoice that you generated based on ['sales',19.5]
and the output of your system gives category C1 and vat rate V1, then do
rouge-1('sales',C1) 
and
rouge-1('19.5',V1)

"""
"""
Presentation:
1. Purpose - (non technical)
2. Example - Show an invoice, and say what we'd want the output to be (non-technical)
3. Show the test set
4. Show a couple of constructed invoices from the test set.
5a. Say settign up the system as API using fastapi.
5b. Show test predict enpoint briefly, explain what it does, not HOW. It calls the fastapi endpoints
5c. Explain how the RAG process works - not technical, but how it builds the prompt using the database; and how
it matches the relevant elements in the database to the query.
6. Start the server main.py, explaining that your using the UVICORN server. This simulates accessing the API over the internet
7. Have a .py file that just runs a single example, and show the results
8. Then run the whole of test_predict_endpoint to get full results
9. Have proper plots and stuff using matplotlib (ask GPT how to do pretty plots and which plots and measures to use)
"""

"""
To run the test set:
load in the csv containing the test set.
Go through each row of the csv:
    pull out column 0 (the json description)
    Send a prompt to GPT-4o saying "Use the following to create a UK invoice, do not include the VAT percentage"
    That will give you a invoice I.
    Pull out column 1 and 2 (VAT rate and category).
    Store I, col1 , col2 in a new "test_set.csv" 
Set up test_set_predict_endpoint.py to loop through test_set.csv
    send col0 of the test set to the 
    predictor. 
    That will then return a prediction of VAT rate Vp and category Cp.
    Then do rouge-1 on Vp vs col1 of the test set and Cp vs col2 of the test set
"""
"""
First csv was the one they sent you.
Second one will look like this:
invoice text, actual VAT, actual category
<long invoice text>, 20, sales
<long invoice text>, 15, marketing
etc
"""
