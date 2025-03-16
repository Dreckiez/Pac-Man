# Pac-Man 🤖

## Documentation
### Command Line
- Từ Level 1-4: chạy theo command line
```bash
python pacman.py <Tên Search Algo> <Số thứ tự Test Case>
```
Example:
```bash
python pacman.py A* 4
```
Ghi sai tên Search sẽ báo lỗi: Invalid Search Algorithm<br>
Ghi sai số thứ tự Test Case (có 5 cái mà ghi 6) báo: Invalid Test Case

- Level 5: Chạy ổn nhưng thỉnh thoảng có vài case UCS hoặc BFS/DFS báo lỗi current = parent[current] ngay khi vào loop => parent[current/Pacman] không có => không biết tại sao
```bash
python pacman.py all
```

- Level 6:
```bash
python pacman.py
```

### Biến
- Pacman_pos_cases, Ghost_pos_cases: 1 list chứa các vị trí được chọn sẵn để lấy data từ các Search
- traverses, path: dùng để lưu những node đã search và path đi từ Ghost đến Pacman
- visualize_search, visualize_path: dùng để visualize thuật toán search và path từ Ghost đến Pacman
- Draw_Search_Event, Draw_Path_Event: dùng để trigger event vẽ search, path
  - Vẽ Search trước
  - Vẽ Path sau 

### Cách Visualize hiện tại
- Từ Level 1-4:
  - Chạy thuật toán trước, lưu list các node đã search và path (Biến traverses, path)
  - Add từng node trong traverses, path vào visualize_search, visualize_path để vẽ lại cách search hoạt động và path
- Level 5:
  - path là mảng 2 chiều: mỗi row lưu 1 path của 1 search algo => có 4 row
  - Ghost_pos là mảng lưu vị trí của 4 Ghost, trigger event Draw_Ghost_Move thì sẽ update Ghost_pos bằng vị trí tiếp theo trong path => Ghost di chuyển theo path
- Level 6:
  - Pacman update vị trí mới thì Ghost update lại Path
