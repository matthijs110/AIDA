yml_schema = {
    'service': {
        'required': True,
        'type': 'dict',
        'schema': {
            'version': {
                'required': True,
                'type': 'string'
            },
            'url': {
                'required': True,
                'type': 'string'
            },
            'srs': {
                'required': True,
                'type': 'string'
            },
            'format': {
                'required': True,
                'type': 'string'
            },
            'transparent': {
                'required': True,
                'type': 'boolean'
            },
            'layer': {
                'required': True,
                'type': 'string'
            }
        }
    },
    'bbox': {
        'required': True,
        'type': 'dict',
        'schema': {
            'west': {
                'required': True,
                'type': 'number'
            },
            'south': {
                'required': True,
                'type': 'number'
            },
            'east': {
                'required': True,
                'type': 'number'
            },
            'north': {
                'required': True,
                'type': 'number'
            } 
        }          
    },
    'image': {
        'required': True,
        'type': 'dict',
        'schema': {
            'tempsize': {
                'required': True,
                'type': 'number'
            },
            'size': {
                'required': True,
                'type': 'number'
            },
            'resolution': {
                'required': True,
                'type': 'number'
            },
            'directory': {
                'required': True,
                'type': 'string'
            },
            'projection': {
                'required': True,
                'type': 'string'
            }
        }
    },
    'timeout': {
        'required': True,
        'type': 'number'
    },
    'bandscount': {
        'required': True,
        'type': 'number'
    },
    'tmpdirectory': {
        'required': True,
        'type': 'string'
    },        
    'threads': {
        'required': True,
        'type': 'number'
    },
}

xml_template = '''<GDAL_WMS>
  <Service name="WMS">
    <Version>%(version)s</Version>
    <ServerUrl>%(url)s</ServerUrl>
    <SRS>%(srs)s</SRS>
    <ImageFormat>image/%(format)s</ImageFormat>
    <Layers>%(layer)s</Layers>
    <transparent>%(transparent)s</transparent>
  </Service>
  <DataWindow>
    <UpperLeftX>%(west)s</UpperLeftX>
    <UpperLeftY>%(north)s</UpperLeftY>
    <LowerRightX>%(east)s</LowerRightX>
    <LowerRightY>%(south)s</LowerRightY>
    <SizeX>%(resolution)s</SizeX>
    <SizeY>%(resolution)s</SizeY>
  </DataWindow>
  <Timeout>%(timeout)s</Timeout>
  <Projection>%(projection)s</Projection>
  <BandsCount>%(bandscount)s</BandsCount>
</GDAL_WMS>'''
