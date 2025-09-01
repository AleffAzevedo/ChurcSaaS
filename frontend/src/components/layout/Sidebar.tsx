'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { cn } from '@/lib/utils';
import { useAuth } from '@/contexts/AuthContext';
import {
  Users,
  UserCheck,
  Calendar,
  DollarSign,
  MessageSquare,
  BarChart3,
  Settings,
  Home,
  Building2,
  Heart,
  BookOpen,
} from 'lucide-react';

interface SidebarItem {
  name: string;
  href: string;
  icon: React.ComponentType<{ className?: string }>;
  description: string;
}

const sidebarItems: SidebarItem[] = [
  {
    name: 'Dashboard',
    href: '/',
    icon: Home,
    description: 'Visão geral do sistema',
  },
  {
    name: 'Membros',
    href: '/membros',
    icon: Users,
    description: 'Gestão de pessoas e famílias',
  },
  {
    name: 'Grupos',
    href: '/grupos',
    icon: UserCheck,
    description: 'Células, classes e ministérios',
  },
  {
    name: 'Eventos',
    href: '/eventos',
    icon: Calendar,
    description: 'Cultos, conferências e atividades',
  },
  {
    name: 'Financeiro',
    href: '/financeiro',
    icon: DollarSign,
    description: 'Receitas, despesas e relatórios',
  },
  {
    name: 'Comunicação',
    href: '/comunicacao',
    icon: MessageSquare,
    description: 'Mensagens e campanhas',
  },
  {
    name: 'Relatórios',
    href: '/relatorios',
    icon: BarChart3,
    description: 'Dashboards e análises',
  },
  {
    name: 'Configurações',
    href: '/configuracoes',
    icon: Settings,
    description: 'Igreja, campus e usuários',
  },
];

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function Sidebar({ isOpen, onClose }: SidebarProps) {
  const pathname = usePathname();
  const { igreja, campus } = useAuth();

  return (
    <>
      {/* Mobile overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 z-40 bg-black bg-opacity-50 lg:hidden"
          onClick={onClose}
        />
      )}

      {/* Sidebar */}
      <div
        className={cn(
          'fixed inset-y-0 left-0 z-50 w-64 bg-white shadow-lg transform transition-transform duration-300 ease-in-out lg:translate-x-0 lg:static lg:inset-0',
          isOpen ? 'translate-x-0' : '-translate-x-full'
        )}
      >
        <div className="flex flex-col h-full">
          {/* Header */}
          <div className="flex items-center justify-between p-4 border-b border-gray-200">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
                <Building2 className="w-5 h-5 text-white" />
              </div>
              <div className="flex flex-col">
                <span className="text-sm font-semibold text-gray-900">
                  {igreja?.nome || 'Igreja SaaS'}
                </span>
                {campus && (
                  <span className="text-xs text-gray-500">{campus.nome}</span>
                )}
              </div>
            </div>
          </div>

          {/* Navigation */}
          <nav className="flex-1 px-4 py-4 space-y-1 overflow-y-auto">
            {sidebarItems.map((item) => {
              const isActive = pathname === item.href || 
                (item.href !== '/' && pathname.startsWith(item.href));
              
              return (
                <Link
                  key={item.name}
                  href={item.href}
                  onClick={onClose}
                  className={cn(
                    'flex items-center px-3 py-2 text-sm font-medium rounded-md transition-colors',
                    isActive
                      ? 'bg-blue-100 text-blue-700'
                      : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900'
                  )}
                >
                  <item.icon
                    className={cn(
                      'mr-3 h-5 w-5',
                      isActive ? 'text-blue-700' : 'text-gray-400'
                    )}
                  />
                  <div className="flex flex-col">
                    <span>{item.name}</span>
                    <span className="text-xs text-gray-500">{item.description}</span>
                  </div>
                </Link>
              );
            })}
          </nav>

          {/* Footer */}
          <div className="p-4 border-t border-gray-200">
            <div className="flex items-center space-x-2 text-xs text-gray-500">
              <Heart className="w-4 h-4 text-red-500" />
              <span>Igreja SaaS v1.0</span>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
