# 5 threads in the hackiest way imaginable
echo {1..5} | xargs -d ' ' -n1 -P5 sh -c 'bash wrap.sh' _
