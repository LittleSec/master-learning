echo "[!] rm share memory"
xargs cat shm_id.txt | ipcrm shm
echo "[!] rm shm_id.txt"
rm shm_id.txt
