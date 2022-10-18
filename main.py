import csv
import json
import requests
from create_table_fpdf2 import PDF
from tabulate import tabulate



def main():
    collection, data = user_bit_validation()
    generated_csv(collection)
    generated_display()
    generated_pdf(data)



def request_info():
    """This function requests data from Binance, returns collected bitcoin symbols."""
    request = requests.get("https://api.binance.com/api/v3/ticker/price")
    response = request.json()

    bitSymbols = []
    for i in response:
        bitSymbols.append(i["symbol"])

    return response, bitSymbols


def user_bit_validation():
    """This function validates user input bitcoin symbols, returns dictionary and list of bitcoin symbols and prices."""
    response, bitSymbols = request_info()
    collection = {}
    datas = [["Bitcoin", "Price"]]

    escape = ""
    while escape != "N":
        bit = input("Enter Bitcoin Symbol: ")
        while bit not in bitSymbols:
            print("Invalid Bitcoin Symbol.")
            bit = input("Enter Bitcoin Symbol: ")

        result = list(filter(lambda coin: coin["symbol"] == bit, response))
        collection.update({result[0]["symbol"]:result[0]["price"]})
        datas.append([result[0]["symbol"], result[0]["price"]])

        escape = input("Do You Want to Add More? [Y/N]: ").upper()

    return collection, datas


def generated_csv(data):
    """This function returns csv file."""
    with open("bitcoin_report.csv", "w") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["bitcoin", "price"])
        for key, value in data.items():
            writer.writerow([key, value])


def generated_display():
    """This function displays information through the console."""
    table = []
    with open("bitcoin_report.csv") as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            table.append({"Bitcoin": row[0], "Price": row[1]})
        print(tabulate(table, tablefmt="grid", headers="firstrow", colalign=("left", "left")))


def generated_pdf(data):
    """This function generated pdf file."""
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Times", size=10)

    pdf.create_table(table_data = data, title="Generated Bitcoin Report Prices", cell_width="even", emphasize_data=["Bitcon", "Price"], emphasize_style="BIU", emphasize_color=(255,0,0))
    pdf.ln()

    pdf.text(x=165, y=280, txt="developed by grgttdln")

    pdf.output("GeneratedBitcoinReportPrices.pdf")



if __name__ == "__main__":
    main()
