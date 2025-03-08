# Pac-Man 🤖

## Documentation
### Command Line
- Từ Level 1-4: chạy theo command line
```bash
python pacman.py <Tên Search Algo> <Số thứ tự Test Case>
```
Example:
```bash
python pacman.py BFS 4
```
Ghi sai tên Search sẽ báo lỗi: Invalid Search Algorithm<br>
Ghi sai số thứ tự Test Case (có 5 cái mà ghi 6) báo: Invalid Test Case

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
- Level 5:??
- Level 6: Không cần Visualize đường đi mà chỉ cần cho Ghost di chuyển theo path
  - Có thể cho Ghost cứ 2s lại update vị trí của Pacman => update path mới => di chuyển theo path mới đó
  - Trong khoảng thời gian 2s ko update sẽ chạy theo path cũ (nếu chưa kịp update path mới mà đã chạy hết path thì sao??)
