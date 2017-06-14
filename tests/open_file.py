import emerge_pipeline
import unittest
import sys
from StringIO import StringIO
import subprocess

class TestHello(unittest.TestCase):
    def test_main(self):
        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out
            #emerge_pipeline.main()
            output = out.getvalue()
            #self.assertRegexpMatches(output, "Starting")
        finally:
            sys.stdout = saved_stdout

    def test_vcfs_exists(self):
        self.assertListEqual(
            emerge_pipeline.check_if_vcf_files_exist(["tests/sample.vcf.gz", "tests/sample2.vcf.gz"]),
            ["tests/sample.vcf.gz", "tests/sample2.vcf.gz"]
        )

    def test_vcf_does_not_exists(self):
        with self.assertRaises(IOError):
            emerge_pipeline.check_if_vcf_files_exist(["tests/sample.vcf.gz", "bad_path"])



class TestFunctional(unittest.TestCase):
    def test_program_starts(self):
        self.assertRegexpMatches(
            #subprocess.check_output(["python emerge_pipeline.py -f tests/sample.vcf.gz"], stderr=subprocess.STDOUT, shell=True),
            subprocess.check_output(["python emerge_pipeline.py -f tests/sample.vcf.gz"], shell=True),
            "Starting annotation pipeline"
        )

    def test_program_is_missing_vcf_file(self):
        self.assertRegexpMatches(
            subprocess.check_output(["python emerge_pipeline.py -f bad path"], shell=True),
            "Error"
        )



if __name__ == '__main__':
    unittest.main()