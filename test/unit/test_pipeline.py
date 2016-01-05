import os
import unittest

import pipeline as pl

HERE = os.path.abspath(os.path.dirname(__file__))

class TestPipeline(unittest.TestCase):
    def setUp(self):
        self.pipeline = pl.Pipeline(
            server='testing',
            settings_file=os.path.join(HERE, 'test_settings.json')
        )

    def test_get_config(self):
        config = self.pipeline.get_config()
        self.assertEquals(config['api_key'], 'FUN FUN FUN')
        self.assertEquals(config['root_url'], 'localhost:9000/')
        self.assertEquals(config['organizations'], {})

    def test_reset_config(self):
        self.pipeline.set_config_from_file(
            'second_testing',
            os.path.join(HERE, 'test_settings.json')
        )
        config = self.pipeline.get_config()
        self.assertEquals(config['api_key'], 'EVEN MORE FUN',)
        self.assertEquals(config['root_url'], 'localhost:9001/',)
        self.assertEquals(config['organizations'], {})

    def test_invalid_config(self):
        with self.assertRaises(pl.InvalidConfigException):
            pl.Pipeline(
                server='NO SERVER',
                settings_file=os.path.join(HERE, 'test_settings.json')
            )

    def test_no_config(self):
        with self.assertRaises(pl.InvalidConfigException):
            pl.Pipeline(
                server='NO SERVER',
                settings_file=os.path.join(HERE, 'NOT-A-VALID-PATH')
            )

    def test_misconfigured_pipeline(self):
        with self.assertRaises(RuntimeError):
            pl.Pipeline().run(None)
        with self.assertRaises(RuntimeError):
            pl.Pipeline().extract(pl.FileExtractor).run(None)
        with self.assertRaises(RuntimeError):
            pl.Pipeline().extract(pl.FileExtractor).run(None)
        with self.assertRaises(RuntimeError):
            pl.Pipeline().extract(pl.FileExtractor).schema(pl.BaseSchema).run(None)
        with self.assertRaises(RuntimeError):
            pl.Pipeline().schema(pl.BaseSchema).load(pl.Datapusher).run(None)

    def test_extractor_args(self):
        self.pipeline.extract(pl.FileExtractor, 1, firstline_headers=False)
        self.assertIn(1, self.pipeline.extractor_args)
        self.assertIn('firstline_headers', self.pipeline.extractor_kwargs)