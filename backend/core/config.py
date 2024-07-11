import os

# Define the base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Define paths
DATA_PATH = os.path.join(BASE_DIR, 'backend', 'data', 'final_df_w_fe.csv')
MODEL_PATH = os.path.join(BASE_DIR, 'backend', 'models', 'xgboost_final.json')
FEATURE_LIST = ['Date', 'Store', 'AvgLastMonthSales', 'AvgLastYearSales', 'AvgPromoSales', 'AvgHolidaySales', 'Open', 'Sales', 'Day', 'Month', 'DayOfWeek', 'WeekOfYear', 'Promo', 'StateHoliday', 'SchoolHoliday', 'CompetitionDistance', 'MonthsSinceCompetitionOpen', 'PromoWeeks', 'Assortment', 'StoreType']
