#ifndef RAII_DISABLE_MENUBAR_H
#define RAII_DISABLE_MENUBAR_H

#include <QMenuBar>

namespace Cedrus
{
    class RAII_DisableMenuBar {
    public:
        /// when you instantiate one of these, we disable m_menuBar
        RAII_DisableMenuBar( QMenuBar * menuBar );
        /// when your object goes out of scope, we enable m_menuBar
        ~RAII_DisableMenuBar();
    private:
        QMenuBar * m_menuBar;
    };
} // end namespace Cedrus

#endif // RAII_DISABLE_MENUBAR_H
