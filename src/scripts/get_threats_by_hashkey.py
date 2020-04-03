import sys

from src.common.base_script import BaseScripts
from src.common.logger import logger
from src.engines.get_engine import ThreatsSearch


def main(override_args=None):
    """Method to start the script"""
    starter = BaseScripts()
    logger.debug(f'START: get_threats_by_hashkey.py')

    # Load initial args
    parser = starter.start('Retrieve threats (as Json) from a list of ids (hashkeys)')
    required_named = parser.add_argument_group('required arguments')
    required_named.add_argument(
        '-i',
        '--input_file',
        help='list of users',
        required=True,
    )
    parser.add_argument(
        '--lost',
        help='saved hashes that were not found',
    )
    if override_args:
        args = parser.parse_args(override_args)
    else:
        args = parser.parse_args()

    # Load api_endpoints and tokens
    threats_list = starter._load_csv(args.input_file)
    endpoint_url, main_url, tokens = starter.load_config(args)

    logger.debug(f'TOTAL: {len(threats_list)} threats found for file: {args.input_file}')
    url_threats = main_url + endpoint_url['endpoints']['threats']
    search_engine_threats = ThreatsSearch(url_threats, main_url, tokens)
    list_threats, list_lost_hashes = search_engine_threats.get_json(threats_list)

    if args.output:
        starter.save_output(args.output, list_threats)
        logger.debug(f'Threats JSON saved in {args.output}\n')
    if args.lost:
        starter.save_output(args.lost, list_lost_hashes)
        logger.debug(f'Threats lost saved in {args.lost}\n')
    logger.debug(f'END: get_threats_by_hashkey.py')


if __name__ == '__main__':
    sys.exit(main())