
⚡ Nhanh Như Chớp - Discord Quiz Bot
Nhanh Như Chớp is a fast-paced, interactive Discord trivia bot inspired by the popular Vietnamese game show. It features a competitive scoring system, automated ranking roles, and easy question management.
Nhanh Như Chớp là một bot giải đố tương tác trên Discord được lấy cảm hứng từ chương trình truyền hình cùng tên. Bot sở hữu hệ thống tính điểm kịch tính, tự động cấp danh hiệu theo thứ hạng và công cụ quản lý câu hỏi dễ dàng.
✨ Features / Tính năng nổi bật
🇬🇧 English
 * Dynamic Rounds: Each game consists of 5 random questions from the database.
 * Scoring System: Get +3 points for a correct answer and -1 point for an incorrect one.
 * Auto-Ranking Roles: Automatically assigns VIP, PRO, and NOOB roles to the Top 3 players on the leaderboard.
 * Smart Hints: Shows the number of characters/words in the answer to help players.
 * Persistent Data: Scores and questions are saved in JSON format, ensuring no data loss on restart.
 * 24/7 Up-time: Integrated with Flask for easy hosting on platforms like Replit.
 * 
🇻🇳 Tiếng Việt
 * Vòng chơi năng động: Mỗi lượt chơi gồm 5 câu hỏi ngẫu nhiên từ cơ sở dữ liệu.
 * Hệ thống điểm số: Trả lời đúng nhận +3 điểm, trả lời sai bị -1 điểm.
 * Danh hiệu tự động: Tự động cấp các vai trò (VIP, PRO, NOOB) cho Top 3 người chơi dẫn đầu Server.
 * Gợi ý thông minh: Hiển thị số lượng từ của đáp án để hỗ trợ người chơi.
 * Dữ liệu bền vững: Điểm số và câu hỏi được lưu dưới dạng JSON, không mất dữ liệu khi khởi động lại.
 * Hoạt động 24/7: Tích hợp Flask để giữ bot luôn online khi treo trên Replit hoặc các server tương tự.
 * 
🛠️ Technical Stack / Công nghệ sử dụng
 * Language: Python 3.8+
 * Library: discord.py (v2.x), Flask
 * Database: JSON files (questions.json, data.json)
 * 
🚀 Installation / Cài đặt
 * Install dependencies / Cài đặt thư viện:
   pip install -r requirements.txt

 * Prepare questions / Chuẩn bị câu hỏi:
   * Add your raw questions to user_questions.txt.
   * Run the import script to generate a standardized JSON file:
   python import_questions.py

 * Set up Token / Cấu hình Token:
   * Set an environment variable DISCORD_BOT_TOKEN or edit the TOKEN variable in bot.py.
   * Thiết lập biến môi trường DISCORD_BOT_TOKEN hoặc sửa trực tiếp trong file bot.py.
 * Run the bot / Chạy Bot:
   python bot.py

🎮 Commands / Lệnh sử dụng
| Command | Description (EN) | Mô tả (VI) |
|---|---|---|
| !start | Start a new round (5 questions) | Bắt đầu vòng chơi mới (5 câu) |
| !stop | Cancel the current round | Hủy vòng chơi hiện tại |
| !next | Skip the current question | Bỏ qua câu hỏi hiện tại |
| !score | Show Top 10 leaderboard | Xem bảng xếp hạng Top 10 |
| !help | Show command list | Hiển thị danh sách lệnh |

📁 File Structure / Cấu trúc thư mục
 * bot.py: The heart of the bot / Mã nguồn chính.
 * import_questions.py: Script to process and deduplicate questions / Công cụ xử lý và lọc trùng câu hỏi.
 * keep_alive.py: Mini web server to prevent the bot from sleeping / Web server giữ bot luôn hoạt động.
 * questions.json: The question database / Cơ sở dữ liệu câu hỏi.
 * data.json: Player scores and statistics / Lưu trữ điểm người chơi.
