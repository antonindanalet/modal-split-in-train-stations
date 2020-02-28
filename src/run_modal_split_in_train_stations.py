from utils_mtmc.get_mtmc_files import get_etappen
import numpy as np
from pathlib import Path


def run_modal_split_in_train_stations():
    df_etappen = get_etappen(2015, selected_columns=['HHNR',  # ID of the person
                                                     'WP',  # weight of the person
                                                     'WEGNR',  # ID of the trip
                                                     'ETNR',  # ID of the trip leg
                                                     'f52900',  # Activity at destination of the trip leg
                                                     'f51300',  # Transport mode of the trip leg
                                                     'Z_X',  # X-coordinate of the destination of the trip leg
                                                     'Z_Y',  # Y-coordinate of the destination of the trip leg
                                                     'Z_Str'])  # Street name of the destination of the trip leg
    df_etappen = define_trips_going_through_the_railway_station(df_etappen)
    groups_in_and_out = define_the_main_transport_mode_per_trip(df_etappen)
    # Compute the weighted average
    sum_of_all_weights = groups_in_and_out['WP'].sum()
    folder_path_output = Path('../data/output/')
    groups_in_and_out.groupby(['f51300']).agg(lambda x: x.sum() / sum_of_all_weights)\
        .to_csv(folder_path_output / 'modal_split_in_Bern_station.csv', sep=';')


def define_the_main_transport_mode_per_trip(df_etappen):
    # Recode transport mode in order of priority, with one being the top priority
    df_etappen['f51300'].replace({17: 1,  # plane
                                  9: 2,  # train
                                  10: 3,  # PostAuto / CarPostal / PostBus
                                  16: 4,  # boat
                                  12: 5,  # tram
                                  11: 6,  # bus
                                  18: 7,  # other public transport?
                                  14: 8,  # autocar
                                  7: 9,  # car as driver
                                  8: 9,  # car as passenger
                                  15: 10,  # truck
                                  13: 11,  # taxi
                                  5: 12,  # motorbike
                                  6: 12,  # motorbike as passenger
                                  4: 13,  # small motorbikes
                                  3: 14,  # cyclomoteur
                                  2: 15,  # bikes
                                  20: 15,  # Ebikes
                                  21: 15,  # Ebikes
                                  1: 16,  # walking
                                  19: 17,  # rollers, trottinettes, skateboards, ...
                                  95: 95}, inplace=True)  # other
    # Define the main transport mode by trip in and out
    groups_trip_legs = df_etappen.groupby(['HHNR', 'WEGNR', 'through_railway_station']).agg({'WP': lambda x: x.iloc[0],
                                                                                             'f51300': 'min'})
    # Group main transport mode
    groups_trip_legs['f51300'].replace({1: 'Autres',  # plane -> other
                                        2: 'Train',  # train -> train
                                        3: 'Transports publics routiers',  # PostAuto -> road PT
                                        4: 'Autres',  # boat -> other
                                        5: 'Transports publics routiers',  # tram -> road PT
                                        6: 'Transports publics routiers',  # bus -> road PT
                                        7: 'Autres',  # other public transport -> other
                                        8: 'Transports publics routiers',  # autocar -> road PT
                                        9: 'Transport individuel motorisé',  # car -> TIM
                                        10: 'Autres',  # truck -> other
                                        11: 'Autres',  # taxi -> other
                                        12: 'Transport individuel motorisé',  # moto -> TIM
                                        13: 'Transport individuel motorisé',  # small motorbikes -> TIM
                                        14: 'Transport individuel motorisé',  # cyclomoter -> TIM
                                        15: 'Vélo (incl. vélo électrique)',
                                        16: 'A pied',
                                        17: 'Autres',
                                        95: 'Autres'}, inplace=True)
    # Consider the transport mode as a tuple: transport modes in and out the station
    groups_in_and_out = groups_trip_legs.groupby(['HHNR', 'WEGNR']).agg({'WP': lambda x: x.iloc[0],
                                                                         'f51300': lambda x: tuple(x)})
    return groups_in_and_out


def define_trips_going_through_the_railway_station(df_etappen):
    define_trip_legs_going_through_the_railway_station(df_etappen)
    define_trip_legs_before_and_after_going_through_the_railway_station(df_etappen)
    df_etappen.drop('f52900', axis=1, inplace=True)  # Remove the activity at destination, not useful anymore
    df_etappen = df_etappen[df_etappen['through_railway_station'] > 0]  # Remove trips not going through the station
    return df_etappen


def define_trip_legs_before_and_after_going_through_the_railway_station(df_etappen):
    # Add 1 in the new column when the trip leg is before the railway station and in the same trip
    df_trips_including_a_stop_at_station = df_etappen.loc[df_etappen['through_railway_station'] == 1,
                                                          ['HHNR', 'WEGNR', 'ETNR']]
    define_trip_legs_before_going_through_the_railway_station(df_etappen, df_trips_including_a_stop_at_station)
    # Add 2 in the new column if the trip leg is after the railway station and in the same trip
    define_trip_legs_after_going_through_the_railway_station(df_etappen, df_trips_including_a_stop_at_station)


def define_trip_legs_after_going_through_the_railway_station(df_etappen, df_trips_including_a_stop_at_station):
    # For all stops at the railway station...
    for index, row in df_trips_including_a_stop_at_station.iterrows():
        trip_leg_number = row['ETNR']
        person_id = row['HHNR']
        trip_id = row['WEGNR']
        still_the_same_trip = True
        while still_the_same_trip:
            trip_leg_number += 1
            # Gets the activity of each trip leg
            activity_at_destination_of_the_trip_leg = df_etappen.loc[(df_etappen['HHNR'] == person_id) &
                                                                     (df_etappen['WEGNR'] == trip_id) &
                                                                     (df_etappen['ETNR'] == trip_leg_number),
                                                                     'f52900']
            if len(activity_at_destination_of_the_trip_leg) > 0:
                index_of_the_trip_leg = activity_at_destination_of_the_trip_leg.index.values[0]
                activity_at_destination_of_the_trip_leg = activity_at_destination_of_the_trip_leg.values[0]
                # If activity at destination of the trip is "changing transport mode", i.e., still the same
                if activity_at_destination_of_the_trip_leg == 1:
                    df_etappen.loc[index_of_the_trip_leg, 'through_railway_station'] = 2
                # If activity at destination of the trip is anything else, still define it as part of the trip...
                else:
                    df_etappen.loc[index_of_the_trip_leg, 'through_railway_station'] = 2
                    # And then stop the process
                    still_the_same_trip = False
            else:
                still_the_same_trip = False


def define_trip_legs_before_going_through_the_railway_station(df_etappen, df_trips_including_a_stop_at_station):
    # For all stops at the railway station...
    for index, row in df_trips_including_a_stop_at_station.iterrows():
        trip_leg_number = row['ETNR']
        person_id = row['HHNR']
        trip_id = row['WEGNR']
        still_the_same_trip = True
        while still_the_same_trip:
            trip_leg_number = trip_leg_number - 1
            if trip_leg_number < 1:
                still_the_same_trip = False
            # Gets the activity of each trip leg
            activity_at_destination_of_the_trip_leg = df_etappen.loc[(df_etappen['HHNR'] == person_id) &
                                                                     (df_etappen['WEGNR'] == trip_id) &
                                                                     (df_etappen['ETNR'] == trip_leg_number),
                                                                     'f52900']
            if len(activity_at_destination_of_the_trip_leg) > 0:
                index_of_the_trip_leg = activity_at_destination_of_the_trip_leg.index.values[0]
                activity_at_destination_of_the_trip_leg = activity_at_destination_of_the_trip_leg.values[0]
                # If activity at destination of the trip is "changing transport mode", i.e., still the same
                if activity_at_destination_of_the_trip_leg == 1:
                    df_etappen.loc[index_of_the_trip_leg, 'through_railway_station'] = 1
                else:
                    still_the_same_trip = False
            else:
                still_the_same_trip = False


def define_trip_legs_going_through_the_railway_station(df_etappen):
    # Create a new column with 1 if the trip leg ends in the train station based on coordinates, 0 otherwise
    df_etappen['through_railway_station'] = np.where((df_etappen['Z_X'] > 7.4369) & (df_etappen['Z_X'] < 7.4406) &
                                                     (df_etappen['Z_Y'] > 46.9474) & (df_etappen['Z_Y'] < 46.9497),
                                                     1, 0)
    # Manual correction: Bollwerk 4 is not the train station
    manual_correction_streets(df_etappen, street_name='Bollwerk')
    # The park above the train station is not the train station
    manual_correction_streets(df_etappen, street_name='PARKTERRASSE')
    # Bubenbergplatz 8 and 10 are not in the train station
    manual_correction_streets(df_etappen, street_name='BUBENBERGPLATZ')
    # Laupenstrasse 2 is a cinema, not in the train station
    manual_correction_streets(df_etappen, street_name='LAUPENSTRASSE')
    # Schanzenstrasse 1 ist not in the train station
    manual_correction_streets(df_etappen, street_name='SCHANZENSTR.')
    # Save the unique points defining the train station for visualization
    saving_unique_points(df_etappen)
    # Remove informations about X-Y coordinates and street name, not useful anymore
    df_etappen.drop(['Z_X', 'Z_Y', 'Z_Str'], axis=1, inplace=True)


def saving_unique_points(df_etappen):
    # Keep only point in the train station
    df_train_station_only = df_etappen[df_etappen['through_railway_station'] == 1]
    # Remove person identification, transport mode and activity. Keep only coordinates and strret name.
    df_train_station_only = df_train_station_only[['Z_X', 'Z_Y', 'Z_Str']]
    # Save every point only once
    folder_path_output = Path('../data/output/')
    df_train_station_only.drop_duplicates().to_csv(folder_path_output / 'unique_points_train_station.csv',
                                                   index=False, sep=';', encoding='iso-8859-15')


def manual_correction_streets(df_etappen, street_name):
    df_etappen.loc[((df_etappen['Z_Str'] == street_name) & (df_etappen['through_railway_station'] == 1)),
                   'through_railway_station'] = 0


if __name__ == '__main__':
    run_modal_split_in_train_stations()
