from flask import Flask, render_template

app = Flask(__name__)

def load_graph_to_png(name_company, file_name):
    m1 = MoexImporter()  
    sec = MoexSecurity(name_company, m1)
    candles_df = sec.getCandleQuotesAsDataFrame(date(2023, 1, 1), date(2024, 1, 24), interval=MoexCandlePeriods.Period1Day, board=None) 
    mpf.plot(candles_df, title=name_company, type="candle", mav=10, style="yahoo", savefig=file_name)

@app.route("/")
def home_page():
    kwargs = dict()
    #
    filename = "list_of_comp" + ".txt"
    file = open(filename)
    companies = file.read()
    comp = companies.split("\n")
    kwargs["stock"] = comp
    #
    return render_template("main_page.html", **kwargs)

@app.route("/company/<name>")
def user(name):
    file = open(f'companies/{name}.txt', 'r')
    company = file.readlines()
    file.close()
    args = company[0].split(" ")
    for i in range(len(args)):
        sym = args[i]
        args[i] = sym[1:len(sym)-1]
    args[-1] = args[-1][0:len(args[-1]) - 1]
    for i in range(1, len(company)):    
        a = company[i].split(" ")
        company[i] = [float(j) for j in a]  
    kwargs = dict()
    kwargs["args"] = args 
    kwargs["ticker"] = company[1:]
    kwargs["name"] = "Sberbank"
    kwargs["id"] = "SBER"
    kwargs["img"] = "SBER.png"
    #load_graph_to_png("SBER", "SBER.png")
    return render_template('stock.html', **kwargs)

if __name__ == "__main__":
    app.run(port=8080, host="127.0.0.1")