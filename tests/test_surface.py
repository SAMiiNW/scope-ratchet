from pathlib import Path
CODE=Path('contracts/contract.py').read_text(encoding='utf-8')
def test_surface():
 for name in ('open_procurement','file_change_order','challenge_measurement','finalize_order','close_procurement','get_procurement','get_order'): assert 'def '+name in CODE
 assert 'projected>=int(p.threshold_bps)' in CODE and "scope_class']=='NEW'" in CODE
 assert 'frozen procurement context changed' in CODE and 'run_nondet_unsafe' in CODE
