# Name: Shailja kashyap
# ERP: 00910
# program: BCA-1C (full stack)
# project: population data visualizer
import pandas as pd
import matplotlib.pyplot as plt


# Load and validate CSV data
def load_data():
    try:
        df = pd.read_csv("population.csv", dtype=str)

        required = ["City", "Year", "Population"]

        if not all(col in df.columns for col in required):
            print("Error: CSV must contain City, Year, Population.")
            return None

        valid_rows = []
        skipped = False

        for index, row in df.iterrows():
            row_no = index + 1

            city = str(row["City"]).strip()
            year = str(row["Year"]).strip()
            population = str(row["Population"]).strip()

            if not city or city.lower() == "nan":
                print(f"Row {row_no} skipped: City is missing.")
                skipped = True
                continue

            try:
                year = int(year)
            except ValueError:
                print(f"Row {row_no} skipped: Invalid Year.")
                skipped = True
                continue

            try:
                population = int(population)
            except ValueError:
                print(
                    f"Row {row_no} skipped: "
                    f"invalid Population '{population}'."
                )
                skipped = True
                continue

            if population <= 0:
                print(
                    f"Row {row_no} skipped: "
                    "Population must be positive."
                )
                skipped = True
                continue

            valid_rows.append({
                "City": city,
                "Year": year,
                "Population": population
            })

        df = pd.DataFrame(valid_rows)

        df = df.drop_duplicates(
            subset=["City", "Year"],
            keep="last"
        )

        if skipped:
            print(f"Valid rows: {len(df)}")

        if df.empty:
            return None

        return df

    except FileNotFoundError:
        print("Error: population.csv file not found.")
        return None

    except pd.errors.EmptyDataError:
        print("Error: CSV file is empty.")
        return None


# Calculate growth percentage
def calculate_growth(df):
    growth_data = []

    for city, group in df.groupby("City"):
        group = group.sort_values("Year")

        first = group.iloc[0]
        last = group.iloc[-1]

        if first["Year"] == last["Year"]:
            continue

        growth = (
            (last["Population"] - first["Population"])
            / first["Population"]
        ) * 100

        growth_data.append({
            "City": city,
            "Growth": growth
        })

    return pd.DataFrame(growth_data)


# Display population summary
def show_summary(df):
    latest_year = df["Year"].max()

    latest_data = df[df["Year"] == latest_year]

    total_population = latest_data["Population"].sum()

    largest_city = latest_data.loc[
        latest_data["Population"].idxmax()
    ]

    if df["Year"].nunique() == 1:
        print(
            f"Total population: {total_population} | "
            f"Largest city: {largest_city['City']}"
        )
        print(
            "Growth: not available (only one year of data)"
        )
        return

    print(
        f"Total population ({latest_year}): "
        f"{total_population}"
    )

    print(
        f"Largest city: {largest_city['City']} "
        f"({largest_city['Population']})"
    )

    growth_df = calculate_growth(df)

    if not growth_df.empty:
        fastest = growth_df.loc[
            growth_df["Growth"].idxmax()
        ]

        print(
            f"Fastest growing: {fastest['City']} "
            f"({fastest['Growth']:+.2f}%)"
        )
    else:
        print("Growth: not available (only one year of data)")


# Display growth and charts
def show_growth_and_charts(df):
    growth_df = calculate_growth(df)

    if growth_df.empty:
        print("Growth: not available (only one year of data)")
        return

    for _, row in growth_df.iterrows():
        print(
            f"{row['City']}: {row['Growth']:+.2f}%"
        )

    # Bar chart
    plt.figure(figsize=(8, 5))

    plt.bar(
        growth_df["City"],
        growth_df["Growth"]
    )

    plt.title("Population Growth by City")
    plt.xlabel("City")
    plt.ylabel("Growth (%)")
    plt.tight_layout()

    # Line chart
    plt.figure(figsize=(8, 5))

    for city, group in df.groupby("City"):
        group = group.sort_values("Year")

        plt.plot(
            group["Year"],
            group["Population"],
            marker="o",
            label=city
        )

    plt.title("Population Trend")
    plt.xlabel("Year")
    plt.ylabel("Population")
    plt.legend()
    plt.tight_layout()

    print("Bar chart 'Population Growth by City' and line chart "
          "'Population Trend' displayed.")

    plt.show()


# Main function
def main():
    print("===== POPULATION DATA VISUALIZER =====")

    df = load_data()

    if df is None:
        return

    print("\n--- MENU ---")
    print("1. Summary")
    print("2. Growth and Charts")

    choice = input("Enter your choice (1 or 2): ")

    if choice == "1":
        show_summary(df)

    elif choice == "2":
        show_growth_and_charts(df)

    else:
        print("Invalid choice. Please select 1 or 2.")


if __name__ == "__main__":
    main()
