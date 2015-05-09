#!/bin/python3
from collections import defaultdict, namedtuple
import shapefile
import json


def _swap_pairs(pair_seq):
    return [(b, a) for (a, b) in pair_seq]

def _b_to_str(s):
    if isinstance(s, bytes):
        return s.decode().strip()
    return s

class ShapeRecord:
    def __init__(self, fields_dict):
        self.plate_id = int(fields_dict['PLATEID1'])
        self.type = _b_to_str(fields_dict['TYPE'])
        self.from_age = float(fields_dict['FROMAGE'])
        self.to_age = float(fields_dict['TOAGE'])
        self.name = _b_to_str(fields_dict['NAME'])
        self.description = _b_to_str(fields_dict['DESCR'])

    def __str__(self):
        return str(self.__dict__)


class ShapefileWrapper:
    def __init__(self, shapefile_path):
        self.json_dump = []
        self.sf = shapefile.Reader(shapefile_path)
        # print(self.sf.fields)

        # record_list = list(self.sf.iterRecords())
        shape_list = list(self.sf.iterShapes())
        # length = len(shape_list)

        # self.types_dict = defaultdict(lambda: 0)
        # for i in range(0, length):
        #     record_type = record_list[i][1]
        #     self.types_dict[record_type] += 1

    def __to_record_dict(self, record):
        """
        :param record: (0-based) list of field values for self.sf.fields.
        :return: A dict for the record: {field_name: field_value}
        """
        record_fields = {f[0]: r for (f,r) in zip(self.sf.fields, ['dummy'] + record)}
        return record_fields

    def record_iter(self):
        """
        :return: An iterator of ShapeRecord-s for the shapefile.
        """
        return [
            ShapeRecord(self.__to_record_dict(r))
            for r in self.sf.iterRecords()
        ]

    def json_obj_iter(self):
        return [
            {'FeatureType': record.type, 'FeatureBegin': record.from_age, 'FeatureEnd': record.to_age,
             'FeatureName': record.name, 'FeaturePoints': _swap_pairs(shape.points)}
            for record, shape in zip(self.record_iter(), self.sf.iterShapes())
        ]


def test(self):
    swapped = _swap_pairs([(1,2), (3,4)])
    assert swapped == [(2,1), (4,3)]


if __name__ == '__main__':
    # test()
    shape_file_path = "./earthbyte/ContinentalPolygons/Shapefile/Seton_etal_ESR2012_ContinentalPolygons_2012.1.shp"
    wrapper = ShapefileWrapper(shape_file_path)
    print('record_iter', '\n'.join([str(r) for r in wrapper.record_iter()]))

    with open('shp.json', 'w') as outfile:
        json.dump(wrapper.json_obj_iter(), outfile, indent=2)
