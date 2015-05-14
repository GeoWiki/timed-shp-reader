#!/bin/python3
import shapefile
import json


def _swap_pairs(pair_seq):
    return [(b, a) for (a, b) in pair_seq]

def _b_to_str(s):
    if isinstance(s, bytes):
        return s.decode().strip()
    return s


class ShapefileWrapper:
    def __init__(self, shapefile_path):
        self.sf = shapefile.Reader(shapefile_path)

    def __to_record_dict(self, record):
        """
        :param record: (0-based) list of field values for self.sf.fields.
        :return: A dict for the record: {field_name: field_value}
        """
        record_fields = {f[0]: _b_to_str(r) for (f,r) in zip(self.sf.fields, ['dummy'] + record)}
        return record_fields

    def record_iter(self):
        """
        :return: An iterator of ShapeRecord-s for the shapefile.
        """
        return [
            self.__to_record_dict(r)
            for r in self.sf.iterRecords()
        ]


class EarthbyteShapeRecord:
    def __init__(self, fields_dict):
        print(fields_dict)
        self.plate_id = int(fields_dict['PLATEID1'])
        self.type = _b_to_str(fields_dict['TYPE'])
        self.from_age = float(fields_dict['FROMAGE'])
        self.to_age = float(fields_dict['TOAGE'])
        self.name = _b_to_str(fields_dict['NAME'])
        self.description = _b_to_str(fields_dict['DESCR'])

    def __str__(self):
        return str(self.__dict__)


def earthbyte_json_iter(sf_wrapper):
    records = [EarthbyteShapeRecord(r) for r in sf_wrapper.record_iter()]
    return [
        {'FeatureType': record.type, 'FeatureBegin': record.from_age, 'FeatureEnd': record.to_age,
         'FeatureName': record.name, 'FeaturePoints': _swap_pairs(shape.points)}
        for record, shape in zip(records, sf_wrapper.sf.iterShapes())
    ]


def test(self):
    swapped = _swap_pairs([(1,2), (3,4)])
    assert swapped == [(2,1), (4,3)]


if __name__ == '__main__':
    # test()
    # shape_file_path = "./earthbyte/ContinentalPolygons/Shapefile/Seton_etal_ESR2012_ContinentalPolygons_2012.1.shp"
    # shape_file_path = "./cshapes/cshapes.shp"
    shape_file_path = "./chgis/v4_time_prov_pgn_utf.shp "
    wrapper = ShapefileWrapper(shape_file_path)

    # print('record_iter', '\n'.join([str(r) for r in wrapper.record_iter()]))
    # country_years = [
    #     {'name': r['CNTRY_NAME'], 'y1': r['COWSYEAR'], 'y2':r['GWSYEAR'],}
    #     for r in wrapper.record_iter()
    # ]
    # country_years = [str(c) for c in sorted(country_years, key=lambda x:x['name'])]
    # print('record_iter', '\n'.join(country_years))
    print('record_iter', '\n'.join([str(c) for c in wrapper.record_iter()]))

    # with open('shp.json', 'w') as outfile:
    #     json.dump(earthbyte_json_iter(wrapper), outfile, indent=2)
