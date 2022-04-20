
import pandas as pd
from Code.Utils.location_utils import LocationUtils
from pandarallel import pandarallel
pandarallel.initialize(progress_bar=True)


if __name__ == '__main__':
    df = pd.read_csv('Data/magicbricks_lr.csv')
    # df_lr = pd.read_csv('Data/magicbricks_lr.csv')

    # df['Location_Score'] = df['url'].apply(lambda x: df_lr[df_lr['url'] == x]['Location_Score'].values[0] if x in df_lr['url'].values else pd.NA)
    # df.to_csv('Data/magicbricks_lr.csv', index=False)

    df['Location_Score'] = df.parallel_apply(lambda x: LocationUtils.get_address_rating(x['Address']) if pd.isna(x['Location_Score']) else x['Location_Score'], axis=1)
    df.to_csv('Data/magicbricks_lr.csv', index=False)
