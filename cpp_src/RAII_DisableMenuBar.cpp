 #include "RAII_DisableMenuBar.h"

namespace Cedrus
{
    RAII_DisableMenuBar::RAII_DisableMenuBar( QMenuBar * menuBar )
    : m_menuBar(menuBar)
    {
        m_menuBar->setEnabled(false);
    }

    RAII_DisableMenuBar::~RAII_DisableMenuBar()
    {
        m_menuBar->setEnabled(true);
    }

} // end namespace Cedrus
