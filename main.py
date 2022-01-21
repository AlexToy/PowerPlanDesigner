from loading_database import loading_database

dcdc_list, psu_list, consumer_list = loading_database()

for dcdc in dcdc_list:
    print(dcdc.name)

for psu in psu_list:
    print(psu.name)

for consumer in consumer_list:
    print(consumer.name)