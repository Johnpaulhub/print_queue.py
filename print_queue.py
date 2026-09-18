from flask import Flask, request, redirect, url_for

app = Flask(__name__)

# In-memory storage for print queue jobs
PRINT_JOBS = [
    {"id": 1, "filename": "Literature_Essay.pdf", "type": "Black & White", "pages": 5, "copies": 2, "total": 30.0, "status": "In Queue"}
]

@app.route('/')
def print_queue_home():
    job_html = ""
    for j in PRINT_JOBS:
        color_border = "#0284c7" if j['status'] == "In Queue" else "#10b981"
        job_html += f'''
        <div style="background: #1b2230; border-radius: 8px; padding: 12px; margin-bottom: 12px; border: 1px solid #2a3447; border-left: 4px solid {color_border}; font-size: 13px;">
            <div style="font-size: 14px; font-weight: bold; color: #fff; margin-bottom: 4px;">📄 {j['filename']}</div>
            <div style="color: #94a3b8; margin-bottom: 6px;">Type: <span style="color:#fff;">{j['type']}</span> | Pages: <span style="color:#fff;">{j['pages']}</span> | Copies: <span style="color:#fff;">{j['copies']}</span></div>
            <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid #2a3447; padding-top: 6px;">
                <span style="color: #38bdf8; font-weight: bold;">Cost: KES {j['total']:.2f}</span>
                <span style="font-size: 11px; background: #1e293b; color: {color_border}; padding: 2px 6px; border-radius: 4px; font-weight: bold;">{j['status']}</span>
            </div>
        </div>
        '''
    
    if not job_html:
        job_html = "<p style='color:#64748b; text-align:center;'>No active print jobs in the queue.</p>"

    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Cyber Print Queue</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{ font-family: sans-serif; background: #121824; color: #fff; margin: 0; padding: 12px; }}
            h2 {{ color: #38bdf8; border-bottom: 2px solid #38bdf8; padding-bottom: 6px; }}
            .card {{ background: #1b2230; padding: 15px; border-radius: 8px; margin-bottom: 15px; border: 1px solid #2a3447; }}
            input, select {{ width: 100%; padding: 10px; margin: 6px 0 12px 0; background: #121824; border: 1px solid #334155; color: #fff; border-radius: 6px; box-sizing: border-box; font-family: sans-serif; }}
            button {{ width: 100%; padding: 12px; background: #059669; color: white; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; }}
        </style>
    </head>
    <body>
        <h2>Cyber Document Print Queue</h2>
        
        <div class="card">
            <h3 style="margin-top:0; color:#10b981; font-size:15px;">Submit New Print Job</h3>
            <form action="/submit" method="POST">
                <label style="font-size:12px; color:#94a3b8;">Document Name / Subject</label>
                <input type="text" name="filename" placeholder="e.g., Assignment.pdf" required>
                
                <label style="font-size:12px; color:#94a3b8;">Print Type</label>
                <select name="print_type">
                    <option value="Black & White">Black & White (3 KES / page)</option>
                    <option value="Color">Color (10 KES / page)</option>
                </select>
                
                <div style="display:flex; gap:10px;">
                    <div style="flex:1;">
                        <label style="font-size:12px; color:#94a3b8;">Page Count</label>
                        <input type="number" name="pages" value="1" min="1" required>
                    </div>
                    <div style="flex:1;">
                        <label style="font-size:12px; color:#94a3b8;">Copies</label>
                        <input type="number" name="copies" value="1" min="1" required>
                    </div>
                </div>
                
                <button type="submit">+ Add to Print Queue</button>
            </form>
        </div>

        <h3 style="color: #38bdf8; margin-top: 20px;">Live Print Queue</h3>
        {job_html}
    </body>
    </html>
    '''

@app.route('/submit', methods=['POST'])
def submit_job():
    filename = request.form.get('filename')
    print_type = request.form.get('print_type')
    pages = int(request.form.get('pages', 1))
    copies = int(request.form.get('copies', 1))
    
    # Calculate price based on type
    rate = 10.0 if print_type == "Color" else 3.0
    total = rate * pages * copies
    
    if filename:
        new_id = len(PRINT_JOBS) + 1
        PRINT_JOBS.append({
            "id": new_id,
            "filename": filename,
            "type": print_type,
            "pages": pages,
            "copies": copies,
            "total": total,
            "status": "In Queue"
        })
    return redirect(url_for('print_queue_home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)
