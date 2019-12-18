from reportlab.lib.styles import ParagraphStyle


def stylesheet():
    styles = {
        'default': ParagraphStyle(
            'default',
            fontName='Helvetica',
            fontSize=12,
            leading=12,
            leftIndent=0,
            rightIndent=0,
            firstLineIndent=0,
            alignment=0,
            spaceBefore=0,
            spaceAfter=0,
            bulletFontName='Times-Roman',
            bulletFontSize=10,
            bulletIndent=0,
            backColor=None,
            wordWrap=None,
            borderWidth=0,
            borderPadding=10,
            borderColor=None,
            borderRadius=None,
            allowWidows=1,
            allowOrphans=0,
            textTransform=None,
            endDots=None,
            splitLongWords=1,
        ),
    }
    styles['title'] = ParagraphStyle(
        'title',
        parent=styles['default'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=42,
        spaceAfter=1,
        underlineProportion=0.09,
        alignment=1,
    )
    styles['graph_title'] = ParagraphStyle(
        'title',
        parent=styles['default'],
        fontSize=18,
        leading=22,
        underlineProportion=0.06,
        alignment=1,
    )
    styles['header'] = ParagraphStyle(
        'alert',
        parent=styles['default'],
        fontSize=18,
        alignment=0,
        underlineProportion=0.06
    )
    styles['second_header'] = ParagraphStyle(
        'alert',
        parent=styles['default'],
        fontSize=14,
        alignment=0,
        underlineProportion=0.06
    )
    styles['footnote'] = ParagraphStyle(
        'footnote',
        parent=styles['default'],
        fontSize=8
    )
    return styles
