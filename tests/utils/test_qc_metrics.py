import json

from BALSAMIC.utils.qc_metrics import (
    get_qc_metrics_json,
    read_metrics,
    update_metrics_dict,
    get_qc_metrics_dict,
)


def test_read_metrics(analysis_path):
    """test metric extraction from a specific QC file"""

    # GIVEN a QC file name
    file_name = "multiqc_picard_dups.json"

    # Given an expected output
    expected_output = {
        "concatenated_tumor_XXXXXX_R": {
            "LIBRARY": "Unknown Library",
            "UNPAIRED_READS_EXAMINED": 11860.0,
            "READ_PAIRS_EXAMINED": 20440841.0,
            "SECONDARY_OR_SUPPLEMENTARY_RDS": 4333388.0,
            "UNMAPPED_READS": 19824.0,
            "UNPAIRED_READ_DUPLICATES": 10178.0,
            "READ_PAIR_DUPLICATES": 14680829.0,
            "READ_PAIR_OPTICAL_DUPLICATES": 0.0,
            "PERCENT_DUPLICATION": 0.718251,
            "ESTIMATED_LIBRARY_SIZE": 5951948.0,
        }
    }

    # WHEN calling the function
    raw_metrics = read_metrics(analysis_path, file_name)

    # THEN check if the extracted metrics correspond to the expected ones
    assert raw_metrics.items() == expected_output.items()


def test_update_metrics_dict():
    """test adding metrics to a nested dictionary"""

    # GIVEN input parameters
    sample_id = "sample_"
    metric = ["test_metric", {"condition": None}]
    value = 0.5

    # Given an expected output
    expected_output = {
        sample_id
        + "1": [
            {"name": "test_metric", "value": value, "condition": None},
            {"name": "test_metric_2", "value": value, "condition": None},
        ],
        sample_id + "2": [{"name": "test_metric_2", "value": value, "condition": None}],
    }

    # WHEN
    # Adding a metric to an empty dictionary
    m_dict = update_metrics_dict(sample_id + "1", metric, value, {})

    # Appending a metric
    metric[0] = "test_metric_2"
    m_dict = update_metrics_dict(sample_id + "1", metric, value, m_dict)

    # Appending a metric from another sample to a dictionary
    m_dict = update_metrics_dict(sample_id + "2", metric, value, m_dict)

    # THEN check if the dictionary is updated correctly
    assert m_dict.items() == expected_output.items()


def test_get_qc_metrics_dict(analysis_path, qc_metrics):
    """test QC metric extraction and its format"""

    # GIVEN a sequencing type
    seq_type = "targeted"

    # GIVEN an expected output
    expected_output = {
        "concatenated_tumor": [
            {
                "name": "MEAN_INSERT_SIZE",
                "value": 74.182602,
                "condition": None,
            },
            {
                "name": "MEAN_TARGET_COVERAGE",
                "value": 832.13854,
                "condition": {"norm": "gt", "threshold": 500.0},
            },
        ]
    }

    # WHEN calling the function
    metrics_dict = get_qc_metrics_dict(analysis_path, qc_metrics["qc"][seq_type])

    # THEN check if the extracted metrics and its structure meets the expected one
    assert metrics_dict.items() == expected_output.items()


def test_get_qc_metrics_json(analysis_path):
    """test JSON object generation"""

    # GIVEN a sequencing type
    seq_type = "targeted"

    # WHEN calling the function
    qc_metrics = get_qc_metrics_json(analysis_path, seq_type)

    # THEN check if the obtained metrics are a valid JSON object
    try:
        json.loads(qc_metrics)
        assert True
    except TypeError:
        assert False
