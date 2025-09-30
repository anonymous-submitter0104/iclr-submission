python dedup.py \
  --file-list "/home/intern/cross_deduplication/paths/test.txt" \
  --output-dir "/home/intern/cross_deduplication/test_output" \
  --hash-file "/home/intern/cross_deduplication/hashes/test_hashes.txt" \
  --log-file "/home/intern/cross_deduplication/errors/test.txt" \
  --hash-algorithm md5 \
  --output-batch-size 20000 \
  --hash-batch-size 10000
