import pandas
import pandas as pd
import matplotlib.pyplot as plt

# source:https://www.imf.org/-/media/Files/Publications/WEO/WEO-Database/2022/WEOApr2022all.ashx
world_economics_path = r"WEOApr2022all.csv"

oecd_countries_iso = ["AUS", "AUT", "BEL", "CAN", "CHL", "CZE", "DNK", "EST", "FIN", "FRA", "DEU", "GRC", "HUN", "ISL",
                      "IRL", "ISR", "ITA", "JPN", "KOR", "LVA", "LUX", "MEX", "NLD", "NZL", "NOR", "POL", "PRT",
                      "SVK", "SVN", "ESP", "SWE", "CHE", "TUR", "GBR", "USA"]

gdp_per_capita_ppp = 'GDP is expressed in constant international dollars per person.'\
                     ' Data are derived by dividing constant price purchasing-power parity (PPP)'\
                     ' GDP by total population.'


Israel_gdp_compare_avg_title = "GDP (PPP) per capita comparison"

AVG_OECD_GDP_ROW = 'Average OECD GDP'
ISRAEL_RANK_ROW = 'Israel Rank (lower is better)'
ISR_PERCENTAGE_OF_AVG_OECD_ROW = 'Israel percentage of average OECD country'
ISRAEL_GDP_ROW = 'Israel GDP'


def calculate_israel_gdp_per_capita_ppp():
    df = pd.read_csv(world_economics_path)
    df = df[df['Subject Notes'] == gdp_per_capita_ppp]  # filter gdp_per_capita_ppp rows

    df = df[df["ISO"].isin(oecd_countries_iso)]  # filter OECD countries rows

    df.append(pandas.Series(name=str(AVG_OECD_GDP_ROW)))
    df.append(pandas.Series(name=ISRAEL_RANK_ROW))
    df.append(pandas.Series(name=ISR_PERCENTAGE_OF_AVG_OECD_ROW))

    for year in range(1995, 2023):
        year = str(year)
        calculate_gdp_per_year(df, year)

    df = filter_df(df)
    df.to_csv("comparison_data.csv")
    plot_data(df.loc[[AVG_OECD_GDP_ROW, ISRAEL_GDP_ROW]], Israel_gdp_compare_avg_title)
    plot_data(df.loc[[ISRAEL_RANK_ROW]], ISRAEL_RANK_ROW, invert_y=True)
    plot_data(df.loc[[ISR_PERCENTAGE_OF_AVG_OECD_ROW]],
              ISR_PERCENTAGE_OF_AVG_OECD_ROW)


def filter_df(df):
    df = df.loc[[AVG_OECD_GDP_ROW, ISRAEL_RANK_ROW, ISR_PERCENTAGE_OF_AVG_OECD_ROW]]\
        .append(df[df["ISO"] == "ISR"])
    df.index = df.index[:-1].append(pd.Index([ISRAEL_GDP_ROW]))
    return df.filter([str(x) for x in range(1995, 2023)])


def plot_data(df, title, invert_y=False):
    t_df_plot = df.T  # for easy plotting we transpose the matrix
    t_df_plot.plot(title=title)
    if invert_y:
        ax = plt.gca()
        ax.invert_yaxis()
    plt.show()


def calculate_gdp_per_year(df, year):
    #  converting value from string to float
    df[year] = df[year].str.replace(',', '')
    df[year] = df[year].astype("float")

    israel_gdp = float(df[df["ISO"] == "ISR"][year])

    # Add to Israel_rank
    df["Rank"] = df[year].rank(ascending=False)
    israel_rank = int(df[df["ISO"] == "ISR"]["Rank"])
    df.loc[ISRAEL_RANK_ROW, year] = israel_rank

    # Add Average row
    avg = df[year].mean()  # mean function returns avg
    df.loc[AVG_OECD_GDP_ROW, year] = round(avg, 2)

    # Add percentage row
    israel_percentage_of_avg_oecd_gdp = round(100 * israel_gdp / avg, 2)
    df.loc[ISR_PERCENTAGE_OF_AVG_OECD_ROW, year] = israel_percentage_of_avg_oecd_gdp

    print(
        f"Israel dgp per capita PPP rank at {year}: {israel_rank} from {str(len(oecd_countries_iso))}"
        f" countries. By percentage compare to average OECD GDP: {str(israel_percentage_of_avg_oecd_gdp)}")
