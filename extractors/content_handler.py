"""Simple content extraction handlers"""

def extract_text(shape) -> str:
    return shape.text.strip()

def extract_table(shape) -> str:
    table = shape.table
    table_content = []
    
    for row in table.rows:
        row_cells = []
        for cell in row.cells:
            cell_text = cell.text.strip()
            if cell_text:
                row_cells.append(cell_text)
        
        if row_cells:
            table_content.append(" | ".join(row_cells))
    
    return "\n".join(table_content)

def extract_chart(shape) -> str:
    try:
        chart = shape.chart
        chart_info = []
        
        if hasattr(chart, 'chart_title') and chart.chart_title.text_frame.text:
            chart_info.append(f"Title: {chart.chart_title.text_frame.text}")
        
        chart_info.append(f"Type: {str(chart.chart_type)}")
        
        if hasattr(chart, 'plots') and chart.plots:
            chart_info.append("Data points detected")
        
        return "\n".join(chart_info)
    except:
        return "[Chart content - data not extractable]"

def extract_smartart(shape) -> str:
    try:
        if hasattr(shape, 'text_frame') and shape.text_frame.text:
            return f"SmartArt: {shape.text_frame.text.strip()}"
        return "[SmartArt graphic]"
    except:
        return "[SmartArt content]"

def extract_textbox(shape) -> str:
    return shape.text_frame.text.strip()

def extract_image(shape) -> str:
    try:
        if hasattr(shape, 'name') and shape.name:
            return f"[Image: {shape.name}]"
        return "[Image content]"
    except:
        return "[Image]"

CONTENT_HANDLERS = {
    'text': extract_text,
    'table': extract_table,
    'chart': extract_chart,
    'image': extract_image,
    'smartart': extract_smartart,
    'textbox': extract_textbox
}